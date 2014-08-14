# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2014

@author: thomas
'''
from django.conf import settings
from django.template.base import TemplateDoesNotExist, Template
from django.template.loader import BaseLoader
from django.utils._os import safe_join
from . import models
from django.utils.translation import ugettext

class DBLoader(BaseLoader):
    is_usable = True
    
    def load_template_source(self, template_name, template_dirs=None):
        try:
            template = models.Template.objects.filter(
                                 enabled=True, 
                                 theme__enabled=True,
                                 path__exact=template_name).order_by('theme__position').first()
        except:
            template = None
        if template is None:
            raise TemplateDoesNotExist()
        return template.source.encode(settings.FILE_CHARSET), 'db_templates://%s' % template.pk
    
    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        template = Template(source)
        return template, origin
        
    load_template_source.is_usable = True