import os
import re

from optparse import OptionParser

from uml2dj.common.parse import parse

def gen_forms(options, logger, args):
    """
    generate django forms from UML xml
       usage: gen_forms <file_name>"""

    if len(args) != 1 or not os.path.isfile(args[0]):
        print "Please specify one correct file for parse"

    models = parse(options, logger, args[0])

    # gen forms 
    for model in models:
        print model.gen_form()
    
