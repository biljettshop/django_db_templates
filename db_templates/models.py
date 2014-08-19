# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2014

@author: thomas
'''
from django.db import models
from django.utils.translation import ugettext_lazy
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save


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
    source = models.TextField(blank=True, default='')
    
    class Meta:
        ordering = ('theme', 'position', 'path')
        
    def __str__(self):
        return "{0}: {1}".format(self.theme, self.path)

@receiver(post_save, sender=Template)
def reset_cached_loader(sender, **kwargs):
    """Resets the cached loader if it finds one in templace_source_loaders
    """
    from django.template.loader import template_source_loaders
    from django.template.loaders.cached import Loader
    for loader in template_source_loaders:
        if isinstance(loader, Loader):
            loader.reset()

class StaticFile(models.Model):
    theme = models.ForeignKey(Theme)
    enabled = models.BooleanField(default=True, db_index=True)
    path = models.CharField(max_length=1024, db_index=True)
    file = models.FileField(upload_to='static_files/%Y/%m/%d', max_length=255)

    class Meta:
        ordering = ('path',)
    
    def __str__(self):
        return "{0}: {1}".format(self.theme, self.path)