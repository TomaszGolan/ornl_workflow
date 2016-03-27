""" Parser for ORNL Workflow Generator """

from datetime import date
import argparse, os

def get_args():
    """ parse command line arguments """
    parser = argparse.ArgumentParser (description = "GENERATE WORKFLOW @ TITAN",
                                      usage = "./generate_workflow.py <opts>",
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    ### REQUIRED ARGUMENT ###

    required = parser.add_argument_group ("REQUIRED ARGUMENTS")

    required.add_argument ("--framework", action = "store", dest = "framework",
                           metavar = "[caffe, theano, ...]",
                           help = "which framework will be used", required=True)

    required.add_argument ("--command", action = "store", dest = "command",
                            metavar = "[./scriptName.py [options]]",
                            help = "main command with options", required = True)

    ### WORKING DIRS ###

    paths = parser.add_argument_group ("WORKING DIRS SETTINGS")

    paths.add_argument ("--framework_dir", action = "store",
                        dest = "framework_dir", metavar = "[PATH]",
                        default = os.environ['PROJWORK'] + "/hep105/software/",
                        help = "path to store framework")

    paths.add_argument ("--software_dir", action = "store",
                        dest = "software_dir", metavar = "[PATH]",
                        default = os.environ['MEMBERWORK'] + "/hep105/software/",
                        help = "path to store software")

    paths.add_argument ("--data_dir", action = "store",
                        dest = "data_dir", metavar = "[PATH]",
                        default = os.environ['PROJWORK'] + "/hep105/data/",
                        help = "path to store data")

    paths.add_argument ("--log_dir", action = "store",
                        dest = "log_dir", metavar = "[PATH]",
                        default = os.environ['MEMBERWORK'] + "/hep105/logs/",
                        help = "path to store logs")

    paths.add_argument ("--output_dir", action = "store",
                        dest = "output_dir", metavar = "[PATH]",
                        default = os.environ['MEMBERWORK'] + "/hep105/output/",
                        help = "path to store output")

    ### INPUT FILES ###

    inputs = parser.add_argument_group ("INPUT FILES / SOFTWARE")

    inputs.add_argument ("--input_data", action = "store", default = "",
                         dest = "input_data", metavar = "[file1 file2 ...]",
                         help = "list of files to get from /proj/hep105/data")

    inputs.add_argument ("--software_list", action = "store",
                         dest = "software_list", metavar = "[/path1/software.list]",
                         default = os.getcwd() + "/software.list",
                         help = "path to a file contains all required software")

    ### OTHER OPTIONS ###

    misc = parser.add_argument_group ("EXTRA OPTIONS")

    misc.add_argument ("--tag", action = "store",
                       dest = "tag", metavar = "[tag]",
                       default = os.environ['USER'] + '_' + str(date.today()),
                       help = "tag used for logs and output files names")

    misc.add_argument ("--force_framework", action = "store_true",
                       dest = "force_framework", default = "false",
                       help = "get framework even if it exists already")

    misc.add_argument ("--force_data", action = "store_true",
                       dest = "force_data", default = "false",
                       help = "get data files even if they exist already")

    misc.add_argument ("--no_archive", action = "store_false",
                       dest = "no_archive", default = "true",
                       help = "do not save files in HPSS after job is done")

    return parser.parse_args()
