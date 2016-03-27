""" Some useful but not interesting functions for ORNL Workflow Generator """

import os, sys

def create_dir(path, tag):
    """ create a single dir and tag subdir """
    if not os.path.exists (path): os.makedirs (path)
    if not os.path.exists (path + '/' + tag): os.makedirs (path + '/' + tag)

def create_dirs(args):
    """ create dirs if needed """
    create_dir(args.framework_dir, args.tag)
    create_dir(args.software_dir, args.tag)
    create_dir(args.data_dir, args.tag)
    create_dir(args.log_dir, args.tag)
    create_dir(args.output_dir, args.tag)

def software_list(framework):
    """ return the list of software required by given framework """
    if framework == "caffe": return ["caffe"]
    if framework == "theano": return ["anaconda2"]
    print "\nERROR: unrecognized framework:", framework
    sys.exit(1)
