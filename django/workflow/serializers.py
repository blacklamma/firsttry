import base64
from backend.config import DATE_TIME_FORMAT
from .models import *
from rest_framework import serializers


class OutgoingEmailsListSerializer(serializers.ModelSerializer):
    queue_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    sent_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    subject = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = OutgoingEmails
        fields = ('id', 'status', 'to_address', 'cc_address', 'bcc_address', 'from_address', 'subject', 'content', 'attached_files',
                  'queue_time', 'sent_time', 'header_message', 'footer_message')

    def get_subject(self, obj):
        try:
            if len(obj.subject) > 40:
                return obj.subject[slice(40)] + '...'
            else:
                return obj.subject
        except Exception as err:
            return ''

    def get_content(self, obj):
        try:
            if len(obj.content) > 40:
                return obj.content[slice(40)] + '...'
            else:
                return obj.content
        except Exception as err:
            return ''


class SMTPSerializer(serializers.ModelSerializer):
    creation_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    last_update_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)

    class Meta:
        model = SMTPConf
        fields = ('id', 'host_name', 'host_username', 'host_email',
                  'host_port', 'creation_time', 'last_update_time')


class IncomingEmailsListSerializer(serializers.ModelSerializer):
    received_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    convert_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    subject = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = IncomingEmails
        fields = ('id', 'status', 'from_address', 'subject', 'content',
                  'attached_files', 'received_time', 'convert_time', 'is_converted')

    def get_subject(self, obj):
        try:
            if len(obj.subject) > 40:
                return obj.subject[slice(40)] + '...'
            else:
                return obj.subject
        except Exception as err:
            return ''

    def get_content(self, obj):
        try:
            if len(obj.content) > 40:
                return obj.content[slice(40)] + '...'
            else:
                return obj.content
        except Exception as err:
            return ''


class EmailToTicketConfSerializer(serializers.ModelSerializer):
    creation_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    last_update_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)

    class Meta:
        model = EmailToTicketConf
        fields = ('id', 'email_id', 'smtp_host_port', 'email_server', 'creation_time',
                  'last_update_time')


class WFListSerializer(serializers.ModelSerializer):
    creation_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    last_update_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    owners = serializers.SerializerMethodField()

    class Meta:
        model = Workflow
        fields = ('id', 'name', 'creation_time', 'last_update_time', 'owners')

    def get_owners(self, obj):
        try:
            return self.context.get('owners').get(obj.id)
        except Exception as err:
            return ''


class StatusListSerializer(serializers.ModelSerializer):
    creation_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    last_update_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    stateName = serializers.CharField(source='state.name', read_only=True)
    stateId = serializers.IntegerField(source='state.id', allow_null=True)
    status_temp = serializers.CharField(source='name', read_only=True)
    stage_temp = serializers.CharField(source='stage', read_only=True)
    wfId = serializers.IntegerField(source='wf.id', read_only=True)

    class Meta:
        model = Status
        fields = ('id', 'state', 'name', 'stage', 'stateName', 'stateId', 'status_temp', 'stage_temp',
                  'creation_time', 'last_update_time', 'wfId')


class RulesListSerializer(serializers.ModelSerializer):
    creation_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    last_update_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    wfId = serializers.IntegerField(source='wf.id', read_only=True)

    class Meta:
        model = Rules
        fields = ('id', 'name', 'if_state', 'if_status', 'if_stage', 'then_state', 'then_status',
                  'creation_time', 'last_update_time', 'wfId', 'is_stage_rule')


class NotificationsListSerializer(serializers.ModelSerializer):
    creation_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    last_update_time = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    wfId = serializers.IntegerField(source='wf.id', read_only=True)

    class Meta:
        model = Notifications
        fields = ('id', 'state', 'status', 'stage', 'subject', 'body',
                  'creation_time', 'last_update_time', 'wfId', 'is_stage_notification')
