# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PartnerMerchant'
        db.create_table(u'partners_partnermerchant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_merchants', to=orm['auth.User'])),
            ('return_trip', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['returntrips.ReturnTrip'], null=True)),
            ('authorization_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('token_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('scope', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('merchant_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('status', self.gf('django_fsm.db.fields.fsmfield.FSMField')(default='pending', max_length=50)),
        ))
        db.send_create_signal(u'partners', ['PartnerMerchant'])


    def backwards(self, orm):
        # Deleting model 'PartnerMerchant'
        db.delete_table(u'partners_partnermerchant')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'partners.partnermerchant': {
            'Meta': {'object_name': 'PartnerMerchant'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'authorization_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'return_trip': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['returntrips.ReturnTrip']", 'null': 'True'}),
            'scope': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'status': ('django_fsm.db.fields.fsmfield.FSMField', [], {'default': "'pending'", 'max_length': '50'}),
            'token_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_merchants'", 'to': u"orm['auth.User']"})
        },
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
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'returning_payload_json': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'status': ('django_fsm.db.fields.fsmfield.FSMField', [], {'default': "'departed'", 'max_length': '50'}),
            'success_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['partners']