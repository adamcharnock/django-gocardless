# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ReturnTrip.cancel_url'
        db.delete_column(u'returntrips_returntrip', 'cancel_url')

        # Deleting field 'ReturnTrip.success_url'
        db.delete_column(u'returntrips_returntrip', 'success_url')

        # Adding field 'ReturnTrip.success_uri'
        db.add_column(u'returntrips_returntrip', 'success_uri',
                      self.gf('django.db.models.fields.URLField')(default='http://dummy.com', max_length=200),
                      keep_default=False)

        # Adding field 'ReturnTrip.cancel_uri'
        db.add_column(u'returntrips_returntrip', 'cancel_uri',
                      self.gf('django.db.models.fields.URLField')(default='http://dummy.com', max_length=200),
                      keep_default=False)

        # Adding field 'ReturnTrip.departure_uri'
        db.add_column(u'returntrips_returntrip', 'departure_uri',
                      self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True),
                      keep_default=False)

        # Adding field 'ReturnTrip.internal_redirect_uri'
        db.add_column(u'returntrips_returntrip', 'internal_redirect_uri',
                      self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ReturnTrip.cancel_url'
        raise RuntimeError("Cannot reverse this migration. 'ReturnTrip.cancel_url' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ReturnTrip.cancel_url'
        db.add_column(u'returntrips_returntrip', 'cancel_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ReturnTrip.success_url'
        raise RuntimeError("Cannot reverse this migration. 'ReturnTrip.success_url' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ReturnTrip.success_url'
        db.add_column(u'returntrips_returntrip', 'success_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200),
                      keep_default=False)

        # Deleting field 'ReturnTrip.success_uri'
        db.delete_column(u'returntrips_returntrip', 'success_uri')

        # Deleting field 'ReturnTrip.cancel_uri'
        db.delete_column(u'returntrips_returntrip', 'cancel_uri')

        # Deleting field 'ReturnTrip.departure_uri'
        db.delete_column(u'returntrips_returntrip', 'departure_uri')

        # Deleting field 'ReturnTrip.internal_redirect_uri'
        db.delete_column(u'returntrips_returntrip', 'internal_redirect_uri')


    models = {
        u'returntrips.returntrip': {
            'Meta': {'object_name': 'ReturnTrip'},
            'cancel_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'departure_uri': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'extra_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'for_model_class': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'for_pk': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_redirect_uri': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'returning_payload_json': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'status': ('django_fsm.db.fields.fsmfield.FSMField', [], {'default': "'departed'", 'max_length': '50'}),
            'success_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['returntrips']