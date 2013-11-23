import os
import re

from optparse import OptionParser

from uml2dj.common.parse import parse

def gen_choices(options, logger, args):
    """
    generate django choices from UML xml
       usage: gen_choices <file_name>"""

    if len(args) != 1 or not os.path.isfile(args[0]):
        print "Please specify one correct file for parse"

    models = parse(options, logger, args[0])
    # print choices
    for model in models:
        for field in model.fields:
            if field.choices:
                print re.sub(r':', ' =', field.choices)
