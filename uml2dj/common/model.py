from uml2dj.common.constants import CHARFIELD_MAX_LENGTH


class Field:
    def __init__(self, name):
        self.name = name
        self.typ = ""
        self.help_text  = ""
        self.choices = ""


class PkField:
    def __init__(self, name):
        self.name = name
        self.point_to = ""
        self.help_text  = ""


class Model:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.fields = []
        self.app_label = ""
        # for pk links to another object
        self.pks = []

    def _gen_header(self):
        meta_string = ""
        appl_label_string = ""
        unicode_string = """
    def __unicode__(self):
        return '%s' % self.id"""
        if self.app_label:
            appl_label_string = "%s" % self.app_label
        if self.name.startswith("Base"):
            meta_string = """
    class Meta:
        abstruct = True"""
        else:
            meta_string = """
    class Meta:
       %s
        verbose_name = "%s" """ % (appl_label_string, self.name)
        if not self.parents:
            return """
class %s(models.Model):
    %s %s""" % (self.name, meta_string, unicode_string)
        else:
            parent_header = ""
            for parent in self.parents:
                parent_header += "%s, " % parent
            return """
class %s(%s):
    %s %s""" % (self.name, parent_header, meta_string, unicode_string)

    def _gen_pk_field(self, name, point_to, **kwargs):
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        if "null" not in kwargs:
            kwargs["null"] = "True"
        kwargs_string = ""
        if kwargs:
            for k, v in kwargs.iteritems():
                kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.ForeignKey(%s, %s)""" % (name, point_to, kwargs_string)
    
    def _gen_char_field(self, name, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = CHARFIELD_MAX_LENGTH
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        if "null" not in kwargs:
            kwargs["null"] = "True"
        kwargs_string = ""
        for k, v in kwargs.iteritems():
            kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.CharField(%s)""" % (name, kwargs_string)

    def _gen_integer_field(self, name, **kwargs):
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        if "null" not in kwargs:
            kwargs["null"] = "True"
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
    %s = models.NullBooleanField(%s)""" % (name, kwargs_string)

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

    def _gen_date_time_field(self, name, **kwargs):
        if "blank" not in kwargs:
            kwargs["blank"] = "True"
        if "null" not in kwargs:
            kwargs["null"] = "True"
        if "auto_now" not in kwargs:
            kwargs["auto_now"]="True"
        kwargs_string = ""
        for k, v in kwargs.iteritems():
            kwargs_string += "%s=%s, " % (k, v)
        return """
    %s = models.DateTimeField(%s)""" % (name, kwargs_string)

    def gen_form(self):
        return """
class %sForm(forms.ModelForm):
    class Meta:
        model = %s """ % (self.name, self.name)

    def gen_admin(self):
        return """
class %sAdmin(admin.ModelAdmin):
    pass

admin.site.register(%s, %sAdmin)""" % (self.name, self.name, self.name)
        
    def gen_fields(self):
        fields_text = "\n"
        for pk_field in self.pks:
            if pk_field.help_text:
                fields_text += self._gen_pk_field(pk_field.name, pk_field.point_to, help_text='_(u"%s")' % pk_field.help_text, verbose_name='_(u"%s")' % pk_field.help_text)
            else:
                fields_text += self._gen_pk_field(pk_field.name, pk_field.point_to)
        for field in self.fields:
            if field.typ == "Char" or field.typ == "String":
                if field.help_text:
                    fields_text += self._gen_char_field(field.name, help_text='_(u"%s")' % field.help_text, verbose_name='_(u"%s")' % field.help_text)
                else:
                    fields_text += self._gen_char_field(field.name)
            if field.typ == "Integer":
                kwargs = {}
                if field.choices:
                    kwargs["choices"] = field.choices.split(":")[0]
                fields_text += self._gen_integer_field(field.name, **kwargs)
            if field.typ == "Boolean":
                fields_text += self._gen_bolean_field(field.name)
            if field.typ == "ByteArray":
                fields_text += self._gen_date_time_field(field.name)
        return "%s %s" % (self._gen_header(), fields_text)
