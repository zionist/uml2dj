from uml2dj.common.constants import CHARFIELD_MAX_LENGTH


class Field:
    def __init__(self, name):
        self.name = name
        self.typ = ""
        self.help_text  = ""


class PkField:
    def __init__(self, name):
        self.name = name
        self.point_to = ""


class Model:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.fields = []
        # for pk links to another object
        self.pks = []

    def _genheader(self, name):
        header = """class %s(models.Model):
    class Meta:
        app_label = "core"
        verbose_name = "%s"
"""
    
    def _gen_char_field(self, name, **kwargs):
        if "max_length" not in kwargs:
            max_length = CHARFIELD_MAX_LENGTH
        else:
            max_length = kwargs["max_length"]
            del kwargs["max_length"]
        kwargs_string = ""
        for k, v in kwargs.iteritems():
            kwargs_string += ", %s=%s" % (k, v)
        return """
        %s = models.CharField(max_length=%s%s) 
        """ % (name, max_length, kwargs_string)

    def _gen_integer_Field(self, name, **kwargs):
        if "default" not in kwargs:
            max_length = CHARFIELD_MAX_LENGTH
        else:
            max_length = kwargs["default"]
            del kwargs["default"]
        kwargs_string = ""
        if kwargs:
            for k, v in kwargs.iteritems():
                kwargs_string += ", %s=%s" % (k, v)
        return """
        %s = models.IntegerField(default=%s%s) 
        """ % (name, default, kwargs_string)

    def gen_fields(self):
        for field in self.fields:
           if field.typ == "Char":
                return self._gen_char_field(field.name, help_text=field.help_text)


        
