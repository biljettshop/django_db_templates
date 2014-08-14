# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Template.text'
        db.delete_column('db_templates_template', 'text')

        # Adding field 'Template.position'
        db.add_column('db_templates_template', 'position',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Template.source'
        db.add_column('db_templates_template', 'source',
                      self.gf('codemirror.fields.CodeMirrorField')(default=''),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Template.text'
        raise RuntimeError("Cannot reverse this migration. 'Template.text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Template.text'
        db.add_column('db_templates_template', 'text',
                      self.gf('codemirror.fields.CodeMirrorField')(),
                      keep_default=False)

        # Deleting field 'Template.position'
        db.delete_column('db_templates_template', 'position')

        # Deleting field 'Template.source'
        db.delete_column('db_templates_template', 'source')


    models = {
        'db_templates.template': {
            'Meta': {'object_name': 'Template'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'source': ('codemirror.fields.CodeMirrorField', [], {}),
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