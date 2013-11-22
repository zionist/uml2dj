#!/usr/bin/env python

import libxml2;
import re
from optparse import OptionParser

USAGE = """Parge uml xml and generate Django model
"""

class Model:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.fields = []
        # for pk links to another object
        self.pks = []


# value of property
def prop_to_str(s):
    s = s.__str__().split("=")[1]
    # remove duoble quotes
    s = re.sub(r'^"|"$', '', s)
    return s
        

def main():
    # all models objects 
    models = []

    parser = OptionParser(USAGE, prog="0.0.1", version="0.0.1")
    parser.add_option("-f", "--file", dest="file", help="xml file for parse")
    options, args = parser.parse_args()
    if not options.file:
        print "Please set -f option"
        exit(1)

    doc = libxml2.parseFile(options.file)
    ctxt = doc.xpathNewContext()
    # for correct work with attrs in different xml namespace
    # for example <packagedElement xsi:type="uml:Class"..
    ctxt.xpathRegisterNs("xmi", "http://www.omg.org/XMI")
    ctxt.xpathRegisterNs("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    for model in ctxt.xpathEval("//packagedElement"):
        model_name = model.hasProp("name")
        if model_name:
            # get name from xml node 
            model_obj = Model(prop_to_str(model_name))
            # find fields
            for field in model.xpathEval("ownedAttribute"):
                typ = field.hasProp("type")
                # We have type attr so this is the link (pk) to another class
                field_name = prop_to_str(field.hasProp("name"))
                # find primary keys to point to
                if typ:
                    typ = prop_to_str(typ)
                    # find packagEdelement with this type
                    el = ctxt.xpathEval('//packagedElement[@xmi:id="%s"]' % typ)
                    pk_name = prop_to_str(el[0].hasProp("name"))
                    model_obj.pks.append({field_name: pk_name})
                # We have no type attr, but we have child type tag for simple type
                else:
                    field.hasProp("name")
                    for simple_type in field.xpathEval("type"):
                        # get type from href attr
                        simple_type = prop_to_str(simple_type.hasProp("href"))
                        m = re.search(r'^.*//(\D+)', simple_type)
                        if m:
                            model_obj.fields.append({field_name: m.group(1)})
            # find parents
            for parent in model.xpathEval("generalization"):
                general = prop_to_str(parent.hasProp("general"))
                parent = ctxt.xpathEval('//packagedElement[@xmi:id="%s"]' % general)
                model_obj.parents.append(prop_to_str(parent[0].hasProp("name")))
                            
        print model_obj.__dict__

                    
            
        #print child.children

    # find parents
    
    #print root

if __name__ == "__main__":
    main()
