# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Template', fields ['enabled']
        db.create_index('db_templates_template', ['enabled'])

        # Adding index on 'Template', fields ['path']
        db.create_index('db_templates_template', ['path'])

        # Adding index on 'Template', fields ['position']
        db.create_index('db_templates_template', ['position'])

        # Adding index on 'StaticFile', fields ['enabled']
        db.create_index('db_templates_staticfile', ['enabled'])

        # Adding index on 'StaticFile', fields ['path']
        db.create_index('db_templates_staticfile', ['path'])

        # Adding index on 'Theme', fields ['enabled']
        db.create_index('db_templates_theme', ['enabled'])

        # Adding index on 'Theme', fields ['name']
        db.create_index('db_templates_theme', ['name'])

        # Adding index on 'Theme', fields ['position']
        db.create_index('db_templates_theme', ['position'])


    def backwards(self, orm):
        # Removing index on 'Theme', fields ['position']
        db.delete_index('db_templates_theme', ['position'])

        # Removing index on 'Theme', fields ['name']
        db.delete_index('db_templates_theme', ['name'])

        # Removing index on 'Theme', fields ['enabled']
        db.delete_index('db_templates_theme', ['enabled'])

        # Removing index on 'StaticFile', fields ['path']
        db.delete_index('db_templates_staticfile', ['path'])

        # Removing index on 'StaticFile', fields ['enabled']
        db.delete_index('db_templates_staticfile', ['enabled'])

        # Removing index on 'Template', fields ['position']
        db.delete_index('db_templates_template', ['position'])

        # Removing index on 'Template', fields ['path']
        db.delete_index('db_templates_template', ['path'])

        # Removing index on 'Template', fields ['enabled']
        db.delete_index('db_templates_template', ['enabled'])


    models = {
        'db_templates.staticfile': {
            'Meta': {'object_name': 'StaticFile'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
        'db_templates.template': {
            'Meta': {'object_name': 'Template'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'default': '0'}),
            'source': ('codemirror.fields.CodeMirrorField', [], {}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
        'db_templates.theme': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'Theme'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'default': '0'})
        }
    }

    complete_apps = ['db_templates']