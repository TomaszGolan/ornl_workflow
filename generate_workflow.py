#!/usr/bin/env python

from parser import get_args
import utils
import pbs
import subprocess

if __name__ == "__main__":
    args = get_args()
    utils.create_dirs(args)
    save_script = pbs.archive_result(args)
    run_script  = pbs.run_job(args, save_script)
    load_script = pbs.load_files(args, run_script)

    print "\n------ GENERATED WORKFLOW SUMMARY ------\n"
    print "Start with:  qsub -q dtn   " + load_script
    print "Which calls: qsub -q titan " + run_script
    print "Which calls: qsub -q dtn   " + save_script
    print "\nTemporary Lustre folders:"
    print "  -framework:\t" + args.framework_dir
    print "  -data:\t" + args.data_dir
    print "  -software:\t" + args.software_dir + "/" + args.tag
    print "  -logs:\t" + args.log_dir + "/" + args.tag
    print "\nOutput, logs and software used will be archived in: " + \
           "/home/$USER/" + args.tag
    print "\n", "-" * 40

    subprocess.Popen ("qsub -q dtn " + load_script, shell=True, executable="/bin/bash")
