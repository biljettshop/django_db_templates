# -*- coding: utf-8 -*-
'''
Created on Aug 14, 2014

@author: thomas
'''
from django import template
from db_templates.models import StaticFile
from django.contrib.sites.models import Site
from django.db.models import Q
from db_templates.hooks import registry as hook_registry

register = template.Library()

@register.simple_tag
def db_templates_static_file(path):
    site = Site.objects.get_current()
    qs = StaticFile.objects.filter(
                                   Q(theme__site__isnull=True) | Q(theme__site=site),
                                   enabled=True, 
                                   theme__enabled=True)
    try:
        obj = qs.get(path=path)
        return obj.file.url
    except:
        return ''

@register.simple_tag(takes_context=True)
def hook(context, name, **kwargs):
    return hook_registry.get_output(name, context, **kwargs)
