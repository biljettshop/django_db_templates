# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Theme'
        db.create_table('db_templates_theme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('db_templates', ['Theme'])

        # Adding model 'Template'
        db.create_table('db_templates_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['db_templates.Theme'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('text', self.gf('codemirror.fields.CodeMirrorField')()),
        ))
        db.send_create_signal('db_templates', ['Template'])


    def backwards(self, orm):
        # Deleting model 'Theme'
        db.delete_table('db_templates_theme')

        # Deleting model 'Template'
        db.delete_table('db_templates_template')


    models = {
        'db_templates.template': {
            'Meta': {'object_name': 'Template'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'text': ('codemirror.fields.CodeMirrorField', [], {}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db_templates.Theme']"})
        },
        'db_templates.theme': {
            'Meta': {'object_name': 'Theme'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['db_templates']