# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payload'
        db.create_table(u'webhook_payload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payload_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resource_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('amount_minus_fees', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('paid_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('signature', self.gf('django.db.models.fields.TextField')()),
            ('received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('json', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'webhook', ['Payload'])


    def backwards(self, orm):
        # Deleting model 'Payload'
        db.delete_table(u'webhook_payload')


    models = {
        u'webhook.payload': {
            'Meta': {'object_name': 'Payload'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'amount_minus_fees': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'flag': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'payload_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'resource_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['webhook']