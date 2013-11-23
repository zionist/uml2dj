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

    def _gen_header(self):
        return """
class %s(models.Model):
    class Meta:
        app_label = "core"
        verbose_name = "%s" """ % (self.name, self.name)
    
    def _gen_char_field(self, name, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = CHARFIELD_MAX_LENGTH
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        kwargs_string = ""
        for k, v in kwargs.iteritems():
            kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.CharField(%s)""" % (name, kwargs_string)

    def _gen_integer_field(self, name, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = 0
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        kwargs_string = ""
        for k, v in kwargs.iteritems():
            kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.IntegerField(%s)""" % (name, kwargs_string)

    def _gen_bolean_field(self, name, **kwargs):
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        kwargs_string = ""
        if kwargs:
            for k, v in kwargs.iteritems():
                kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.BooleanField(%s)""" % (name, kwargs_string)

    def _gen_date_field(self, name, **kwargs):
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        if "null" not in kwargs:
            kwargs["null"] = "True"
        kwargs_string = ""
        for k, v in kwargs.iteritems():
            kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.DateField(%s)""" % (name, kwargs_string)

    def gen_fields(self):
        fields_text = ""
        for field in self.fields:
            # print field.__dict__
            if field.typ == "Char" or field.typ == "String":
                if field.help_text:
                    fields_text += self._gen_char_field(field.name, help_text=field.help_text)
                else:
                    fields_text += self._gen_char_field(field.name)
            if field.typ == "Integer":
                    fields_text += self._gen_integer_field(field.name)
            if field.typ == "Boolean":
                    fields_text += self._gen_bolean_field(field.name)
        print self._gen_header()
        print fields_text
