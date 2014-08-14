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
from django import forms

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'theme', 'path')
    formfield_overrides = {
                           CodeMirrorField: {
                             'widget': CodeMirrorTextarea(mode='django')
                           }
    }
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            return forms.fields.Field(widget=CodeMirrorTextarea(
                                                                mode={"name": "Jinja2"}
                                                                ))
        return admin.TabularInline.formfield_for_dbfield(self, db_field, **kwargs)
admin.site.register(Template, TemplateAdmin)

class TemplateInline(admin.TabularInline):
    model = Template
    extra = 1
    formfield_overrides = {
                           CodeMirrorField: {
                             'widget': widgets.Textarea#CodeMirrorTextarea(mode='django')
                           }
    }
    
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'name')
    #inlines = [TemplateInline]
    pass
admin.site.register(Theme, ThemeAdmin)

