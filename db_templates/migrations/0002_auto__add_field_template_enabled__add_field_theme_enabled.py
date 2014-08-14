# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Template.enabled'
        db.add_column('db_templates_template', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Theme.enabled'
        db.add_column('db_templates_theme', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Template.enabled'
        db.delete_column('db_templates_template', 'enabled')

        # Deleting field 'Theme.enabled'
        db.delete_column('db_templates_theme', 'enabled')


    models = {
        'db_templates.template': {
            'Meta': {'object_name': 'Template'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'text': ('codemirror.fields.CodeMirrorField', [], {}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
        'db_templates.theme': {
            'Meta': {'object_name': 'Theme'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['db_templates']