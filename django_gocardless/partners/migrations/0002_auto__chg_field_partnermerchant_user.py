# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PartnerMerchant.user'
        db.alter_column(u'partners_partnermerchant', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth_custom.User']))

    def backwards(self, orm):

        # Changing field 'PartnerMerchant.user'
        db.alter_column(u'partners_partnermerchant', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

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
        u'auth_custom.user': {
            'Meta': {'ordering': "['-created']", 'object_name': 'User'},
            'can_receive_money': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'hidden_events': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Event']", 'symmetrical': 'False'}),
            'id': ('thisison.utils.models.PkField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'throttle_multiplier': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
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
        u'events.event': {
            'Meta': {'ordering': "['-current_until']", 'object_name': 'Event'},
            'contact_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth_custom.User']"}),
            'current_until': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('thisison.utils.models.HTMLField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'embed_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'featured_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'event_featured_images'", 'null': 'True', 'default': 'None', 'to': u"orm['uploads.Upload']", 'blank': 'True', 'unique': 'True'}),
            'featured_role': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'featured_on'", 'null': 'True', 'default': 'None', 'to': u"orm['events.UserRole']", 'blank': 'True', 'unique': 'True'}),
            'gift_accept_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gift_accept_money': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gift_accept_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gift_accept_words': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gift_email_message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'gift_money_message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'gift_time_message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'gift_words_message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('thisison.utils.models.PkField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'event_images'", 'default': 'None', 'to': u"orm['uploads.Upload']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'involved_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'involved_with'", 'to': u"orm['auth_custom.User']", 'through': u"orm['events.InvolvedUser']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'max_price': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'min_price': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'points': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'roles_external': ('thisison.utils.models.SetField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('thisison.utils.models.HTMLField', [], {}),
            'soundcloud_url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('thisison.utils.models.SetField', [], {'null': 'True', 'blank': 'True'}),
            'ticket_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ticketing_type': ('django.db.models.fields.CharField', [], {'default': "'free'", 'max_length': '16', 'db_index': 'True'}),
            'type_tags': ('thisison.utils.models.SetField', [], {'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'events.involveduser': {
            'Meta': {'object_name': 'InvolvedUser'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'involved_user_links'", 'to': u"orm['events.Event']"}),
            'id': ('thisison.utils.models.PkField', [], {'primary_key': 'True'}),
            'involvement': ('django.db.models.fields.SmallIntegerField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'involvements'", 'to': u"orm['auth_custom.User']"})
        },
        u'events.userrole': {
            'Meta': {'unique_together': "(('role', 'event', 'user'),)", 'object_name': 'UserRole'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['events.Event']"}),
            'id': ('thisison.utils.models.PkField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['auth_custom.User']"})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_merchants'", 'to': u"orm['auth_custom.User']"})
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
        },
        u'uploads.upload': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Upload'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth_custom.User']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('thisison.utils.models.PkField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '10'})
        }
    }

    complete_apps = ['partners']