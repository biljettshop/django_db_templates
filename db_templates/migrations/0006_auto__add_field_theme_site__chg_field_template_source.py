# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Theme.site'
        db.add_column('db_templates_theme', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['sites.Site']),
                      keep_default=False)


        # Changing field 'Template.source'
        db.alter_column('db_templates_template', 'source', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Deleting field 'Theme.site'
        db.delete_column('db_templates_theme', 'site_id')


        # Changing field 'Template.source'
        db.alter_column('db_templates_template', 'source', self.gf('codemirror.fields.CodeMirrorField')())

    models = {
        'db_templates.staticfile': {
            'Meta': {'ordering': "('path',)", 'object_name': 'StaticFile'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '1024'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
        'db_templates.template': {
            'Meta': {'ordering': "('theme', 'position', 'path')", 'object_name': 'Template'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '1024'}),
            'position': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'default': '0'}),
            'source': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
        'db_templates.theme': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'Theme'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'position': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['db_templates']