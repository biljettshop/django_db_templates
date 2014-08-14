# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2014

@author: thomas
'''
from django.db import models
from django.utils.translation import ugettext_lazy
from codemirror.fields import CodeMirrorField
from django.conf import settings
from codemirror.widgets import CodeMirrorTextarea

class Theme(models.Model):
    enabled = models.BooleanField(default=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True,
        verbose_name=ugettext_lazy("Name"),
        help_text=ugettext_lazy("Enter the theme's name."))
    position = models.IntegerField(default=0, db_index=True)
    
    class Meta:
        ordering = ('position', 'name')
        
    def __str__(self):
        return self.name
    
class Template(models.Model):
    theme = models.ForeignKey(Theme)
    enabled = models.BooleanField(default=True, db_index=True)
    path = models.CharField(max_length=1024, db_index=True)
    position = models.IntegerField(default=0, db_index=True)
    if 'codemirror' in settings.INSTALLED_APPS:
        source = CodeMirrorField()
    else:
        source = models.TextField()
    
    class Meta:
        ordering = ('position', 'path')
        
    def __str__(self):
        return "{0}: {1}".format(self.theme, self.path)

class StaticFile(models.Model):
    theme = models.ForeignKey(Theme)
    enabled = models.BooleanField(default=True, db_index=True)
    path = models.CharField(max_length=1024, db_index=True)
    file = models.FileField(upload_to='static_files/%Y/%m/%d', max_length=255)

    class Meta:
        ordering = ('path',)
    
    def __str__(self):
        return "{0}: {1}".format(self.theme, self.path)