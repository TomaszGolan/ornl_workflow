""" Tools for creating PBS scripts for ORNL Workflow Generator """

from utils import software_list
import os

def load_files(args, run):
    """ generate dtn script to load input files and software """
    filename = args.log_dir + '/' + args.tag + "/load_" + args.tag + ".pbs"
    f = open(filename, 'w')

    print >> f, "### PBS DIRECTIVES ###\n"
    print >> f, "#PBS -A hep105"
    print >> f, "#PBS -l nodes=1,walltime=02:00:00" # maximum time for 1 node
    print >> f, "#PBS -j oe"                        # merge out and err
    print >> f, "#PBS -o " + filename + ".out"      # load files log

    print >> f, "\n### GETTING DATA ###\n"

    required_data = args.input_data.split() # list of required data files

    print >> f, "cd " + args.data_dir # can't htar file to specific folder
                                      # need to cd first

    for rd in required_data: # get missing software or update if force used
        if args.force_data or not os.path.isfile (args.data_dir + "/" + rd):
            print >> f, "hsi get /proj/hep105/data/" + rd

    print >> f, "\n### GETTING FRAMEWORK ###\n"

    required_framework = software_list(args.framework) # list of framework libs

    print >> f, "cd " + args.framework_dir # can't htar file to specific folder
                                           # need to cd first

    for rf in required_framework: # get missing software or update if force used
        if args.force_framework or not os.path.exists (args.software_dir + "/" + rf):
            print >> f, "htar -xf /proj/hep105/software/" + rf + ".htar"

    print >> f, "\n### COPYING SOFTWARE ###\n"

    with open(args.software_list, 'r') as in_file: # read list of software
        required_software = in_file.read()

    required_software = required_software.split()

    print >> f, "cd " + args.software_dir + "/" + args.tag # unique for a job

    for rs in required_software: # get software
        print >> f, "cp " + rs + " ."

    print >> f, "\n### CALL RUN SCRIPT ###\n"

    print >> f, "qsub -q titan " + run

    return filename

def run_job (args, put):
    """ generate titan script to run a job """
    filename = args.log_dir + '/' + args.tag + "/run_" + args.tag + ".pbs"
    f = open(filename, 'w')

    print >> f, "### PBS DIRECTIVES ###\n"
    print >> f, "#PBS -A hep105"
    print >> f, "#PBS -l nodes=3750,walltime=24:00:00" # min nodes for day job
    print >> f, "#PBS -j oe"                           # merge out and err
    print >> f, "#PBS -o " + filename + ".out"         # load files log

    print >> f, "\n### SETUP FRAMEWORK ###\n"

    if args.framework == "theano":
        # keep theano compiled code here
        theanoLog = args.log_dir + "/" + args.tag + "/theano"
        if not os.path.exists (theanoLog): os.makedirs (theanoLog)
        # setup libs
        print >> f, "module load cudatoolkit"
        print >> f, "export PATH=" + args.framework_dir + "/anaconda2/bin/:$PATH"
        print >> f, "export THEANO_FLAGS='device=gpu,floatX=float32,compiledir=" + theanoLog + "'"

    print >> f, "\n### RUN A JOB ###\n"

    print >> f, "cd " + args.software_dir + "/" + args.tag
    print >> f, "aprun " + args.command

    if args.no_archive:
        print >> f, "\n### CALL PUT SCRIPT"
        print >> f, "qsub -q dtn " + put

    return filename

def archive_result(args):
    """ save results in HPSS """
    filename = args.log_dir + '/' + args.tag + "/put_" + args.tag + ".pbs"
    f = open(filename, 'w')

    print >> f, "### PBS DIRECTIVES ###\n"
    print >> f, "#PBS -A hep105"
    print >> f, "#PBS -l nodes=1,walltime=02:00:00" # maximum time for 1 node
    print >> f, "#PBS -j oe"                        # merge out and err
    print >> f, "#PBS -o " + filename + ".out"      # load files log

    archive_path = "/home/$USER/" + args.tag # save all in user archive area
    log_path  = archive_path + "/logs/"
    soft_path = archive_path + "/soft/"
    out_path  = archive_path + "/output"

    print >> f, "hsi mkdir " + archive_path
    print >> f, "hsi mkdir " + log_path
    print >> f, "hsi mkdir " + soft_path
    print >> f, "hsi mkdir " + out_path

    sleep 60 # wait for run.pbs.out

    print >> f, "\n### ARCHIVE ALL ###\n"

    print >> f, "cd " + args.log_dir + '/' + args.tag
    print >> f, 'hsi "cd ' + log_path + '; put -R *"'

    print >> f, "cd " + args.software_dir + '/' + args.tag
    print >> f, 'hsi "cd ' + soft_path + '; put -R *"'

    print >> f, "cd " + args.output_dir + '/' + args.tag
    print >> f, 'hsi "cd ' + out_path + '; put -R *"'

    return filename
