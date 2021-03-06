# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2014

@author: thomas
'''
from django.contrib import admin
from .models import Theme, Template
from codemirror.widgets import CodeMirrorTextarea
from django import forms, template
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy
from django.http.response import HttpResponse
import zipfile
from django.conf import settings
from django.conf.urls import url
import io
from db_templates.models import StaticFile
from db_templates.forms import AddThemeAdminForm
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile

try:
    from django_ace import AceWidget
    USE_ACE_WIDGET = True
except:
    USE_ACE_WIDGET = False
    
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
    save_as = True
    search_fields = ('theme__name', 'path')
    fieldsets = (
                 (None, {
                         "fields": (("theme", "enabled", "path", "position"),)
                         }),
                 (None, {
                        "fields": ("source",)
                        })
                 )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if USE_ACE_WIDGET and db_field.name == 'source':
            return TemplateField(widget=AceWidget(
                   mode="django",
                   width="100%",
                   height="50vh",
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

class StaticFileInline(admin.TabularInline):
    model = StaticFile
    extra = 0
    
class StaticFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'theme', 'path')
admin.site.register(StaticFile, StaticFileAdmin)

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'name', 'site', 'get_download_link')
    inlines = [TemplateInline, StaticFileInline]
    form = AddThemeAdminForm
    save_on_top = True
    
    def get_urls(self):
        urls = super(ThemeAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/download-theme/$', 
                self.admin_site.admin_view(self.download_theme),
                name='download-theme'),
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
                filename = "static/{path}".format(
                   path=static_file.path,
                   pk=static_file.pk,
                   enabled=static_file.enabled)
                content = static_file.file.read()
                if static_file not in static_files:
                    z.writestr(filename, content)
                    static_files.append(static_file)
        response = HttpResponse(content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s_theme.zip' % theme.name.lower()
        response.write(s.getvalue())
        return response
    
    def save_model(self, request, obj, form, change):
        admin.ModelAdmin.save_model(self, request, obj, form, change)
        if form.cleaned_data["zip_file"] is not None:
            # Read the zip file and create template files
            with zipfile.ZipFile(request.FILES['zip_file'], mode="r") as zip:
                for name in zip.namelist():
                    if name.startswith('templates/'):
                        source = zip.open(name, "r").read()
                        Template.objects.create(theme=obj,
                                                path=name[10:],
                                                source=source)
                    if name.startswith('static/'):
                        source = UploadedFile(zip.open(name, "r"))
                        StaticFile.objects.create(theme=obj,
                                                  path=name[7:],
                                                  file=source)
admin.site.register(Theme, ThemeAdmin)