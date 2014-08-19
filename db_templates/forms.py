# -*- coding: utf-8 -*-
'''
Created on Aug 19, 2014

@author: thomas
'''
from django import forms
from db_templates.models import Theme
from django.utils.translation import ugettext_lazy

class AddThemeAdminForm(forms.ModelForm):
    zip_file = forms.FileField(required=False,
                               help_text=ugettext_lazy("Import templates from zip-file."))
    class Meta:
        model = Theme