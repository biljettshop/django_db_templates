# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StaticFile'
        db.create_table('db_templates_staticfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['db_templates.Theme'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
        ))
        db.send_create_signal('db_templates', ['StaticFile'])


    def backwards(self, orm):
        # Deleting model 'StaticFile'
        db.delete_table('db_templates_staticfile')


    models = {
        'db_templates.staticfile': {
            'Meta': {'object_name': 'StaticFile'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
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