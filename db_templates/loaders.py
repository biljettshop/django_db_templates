# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2014

@author: thomas
'''
from django.conf import settings
from django.template.base import TemplateDoesNotExist, Template, Origin,\
    StringOrigin
from django.template.loader import BaseLoader, LoaderOrigin, make_origin
from django.utils._os import safe_join
from . import models
from django.utils.translation import ugettext
from django.contrib.sites.models import Site
from django.db.models import Q

class DBOrigin(LoaderOrigin):
    def __init__(self, display_name, loader, name, dirs, source):
        LoaderOrigin.__init__(self, display_name, loader, name, dirs)
        self.source = source
        
    def reload(self):
        return self.source

class DBLoader(BaseLoader):
    is_usable = True
    
    def load_template_source(self, template_name, template_dirs=None):
        try:
            site = Site.objects.get_current()
            template = models.Template.objects.filter(
                                 Q(theme__isnull=True) | Q(theme__site=site),
                                 enabled=True, 
                                 theme__enabled=True,
                                 path__exact=template_name).order_by('theme__position').first()
        except:
            template = None
        if template is None:
            raise TemplateDoesNotExist()
        return template.source, 'db_templates://%s/%s/%s' % (template.pk, template.theme.name, template.path)
    load_template_source.is_usable = True
        
    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        origin = DBOrigin(display_name=origin, 
            loader=self,
            name=template_name,
            dirs=template_dirs, source=str(source))
        
        template = Template(source, origin=origin, name=template_name)
        return template, origin
        
