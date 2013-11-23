import re
import os
import libxml2;
from optparse import OptionParser

from uml2dj.common.model import Model, Field, PkField

# value of property
def prop_to_str(s):
    s = s.__str__().split("=")[1]
    # remove duoble quotes
    s = re.sub(r'^"|"$', '', s)
    # remove html tags for help_text
    s = re.sub(r'&lt.*$', '', s)
    return s

def parse(options, logger, args):
    """
    parse - parse UML 2.0 xml file and write django models
       usage: parse <file_name>"""
    
    if len(args) != 1 or not os.path.isfile(args[0]):
        print "Please specify one correct file for parse"

    base_models = []
    child_models = []
    doc = libxml2.parseFile(args[0])
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
                # find primary keys to point to
                if typ:
                    typ = prop_to_str(typ)
                    # find packagEdelement with this type
                    el = ctxt.xpathEval('//packagedElement[@xmi:id="%s"]' % typ)
                    pk_field_obj = PkField(prop_to_str(field.hasProp("name")))
                    # Find all comments and convert them to help_text
                    comment = field.xpathEval("ownedComment")
                    if comment:
                        pk_field_obj.help_text = ('"%s"' % prop_to_str(comment[0].hasProp("body")))
                    pk_field_obj.point_to = prop_to_str(el[0].hasProp("name"))
                    model_obj.pks.append(pk_field_obj)
                # We have no type attr, but we have child type tag for simple type
                else:
                    field_obj = Field(prop_to_str(field.hasProp("name")))
                    # Find all comments and convert them to help_text
                    comment = field.xpathEval("ownedComment")
                    if comment:
                        field_obj.help_text = ('"%s"' % prop_to_str(comment[0].hasProp("body")))
                    for simple_type in field.xpathEval("type"):
                        # get type from href attr
                        simple_type = prop_to_str(simple_type.hasProp("href"))
                        m = re.search(r'^.*//(\D+)', simple_type)
                        if m:
                            field_obj.typ = m.group(1)
                            model_obj.fields.append(field_obj)
            # find parents
            for parent in model.xpathEval("generalization"):
                general = prop_to_str(parent.hasProp("general"))
                parent = ctxt.xpathEval('//packagedElement[@xmi:id="%s"]' % general)
                model_obj.parents.append(prop_to_str(parent[0].hasProp("name")))
        if model_obj.name.startswith("Base"):
            base_models.append(model_obj)
        else:
            child_models.append(model_obj)
    # sort models. Base classes first
    for model in base_models:
        print model.gen_fields()
    for model in child_models:
        print model.gen_fields()
