# -*- coding: utf-8 -*-
'''
Created on Aug 14, 2014

@author: thomas
'''
from django import template
from db_templates.models import StaticFile

register = template.Library()

@register.simple_tag
def db_templates_static_file(path):
    qs = StaticFile.objects.filter(enabled=True, theme__enabled=True)
    try:
        obj = qs.get(path=path)
        return obj.file.url
    except:
        return ''