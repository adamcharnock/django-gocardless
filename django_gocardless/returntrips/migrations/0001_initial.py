# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReturnTrip'
        db.create_table(u'returntrips_returntrip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('for_model_class', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('for_pk', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django_fsm.db.fields.fsmfield.FSMField')(default='departed', max_length=50)),
            ('extra_state', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('depart_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('success_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('cancel_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('returning_payload_json', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'returntrips', ['ReturnTrip'])


    def backwards(self, orm):
        # Deleting model 'ReturnTrip'
        db.delete_table(u'returntrips_returntrip')


    models = {
        u'returntrips.returntrip': {
            'Meta': {'object_name': 'ReturnTrip'},
            'cancel_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'depart_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'extra_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'for_model_class': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'for_pk': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'returning_payload_json': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'status': ('django_fsm.db.fields.fsmfield.FSMField', [], {'default': "'departed'", 'max_length': '50'}),
            'success_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['returntrips']