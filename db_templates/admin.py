# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2014

@author: thomas
'''
from django.contrib import admin
from .models import Theme, Template
from codemirror.fields import CodeMirrorField, CodeMirrorFormField
from codemirror.widgets import CodeMirrorTextarea
from django.forms import widgets
from django.forms.fields import CharField
from django import forms, template
from django.template.context import RequestContext
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy
from django.http.response import HttpResponse
import zipfile
from _pyio import StringIO
from django.conf import settings
from django.conf.urls import url
import io
from db_templates.models import StaticFile

class TemplateField(forms.fields.Field):
    def validate(self, value):
        forms.fields.Field.validate(self, value)
        try:
            template.Template(value)
        except Exception as e:
            raise ValidationError(e)
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.widget.attrs['rows'] = 120
            
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'theme', 'position', 'path')
    save_on_top = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'source':
            return TemplateField(widget=CodeMirrorTextarea(
               mode={"name": "jinja2"}
            ))
        return admin.TabularInline.formfield_for_dbfield(self, db_field, **kwargs)
admin.site.register(Template, TemplateAdmin)

class TemplateInline(admin.TabularInline):
    model = Template
    fields = ('position', 'path', 'get_edit_link')
    readonly_fields = ('get_edit_link',)
    extra = 0
    
    def get_edit_link(self, obj):
        return '<a href="{url}">{text}</a>'.format(
           url=reverse('admin:db_templates_template_change', args=(obj.pk,)),
           text=ugettext("Edit template"))
    get_edit_link.allow_tags = True
    
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'name', 'get_download_link')
    inlines = [TemplateInline]
    
    def get_urls(self):
        urls = super(ThemeAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/download-theme/$', 
                self.admin_site.admin_view(self.download_theme),
                name='download-theme')
        ]
        return my_urls + urls
    
    def get_download_link(self, obj):
        return '<a href="{url}">{text}</a>'.format(
           url=reverse('admin:download-theme', args=(obj.pk,)),
           text=ugettext("Download theme"))
    get_download_link.allow_tags = True
    get_download_link.short_description = ugettext_lazy("Actions")
    
    def download_theme(self, request, pk):
        theme = Theme.objects.get(pk=pk)
        s = io.BytesIO()
        with zipfile.ZipFile(s, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            templates = []
            for template in theme.template_set.filter(enabled=True):
                filename = "templates/{path}".format(
                   path=template.path,
                   pk=template.pk,
                   position=template.position,
                   enabled=template.enabled)
                if template not in templates:
                    z.writestr(filename, template.source.encode(settings.FILE_CHARSET))
                    templates.append(template)
            static_files = []
            for static_file in theme.staticfile_set.filter(enabled=True):
                filename = "static_files/{path}".format(
                   path=static_file.path,
                   pk=static_file.pk,
                   enabled=static_file.enabled)
                content = static_file.file.read()
                if static_file not in static_files:
                    z.writestr(filename, content)
                    static_files.append(static_file)
        response = HttpResponse(mimetype="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s-Theme.zip' % theme.name
        response.write(s.getvalue())
        return response
        
admin.site.register(Theme, ThemeAdmin)

class StaticFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'theme', 'path')
admin.site.register(StaticFile, StaticFileAdmin)