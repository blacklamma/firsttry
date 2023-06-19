from django.db import models
from django.contrib.auth.models import User


class SMTPConf(models.Model):
    host_name = models.CharField(max_length=100)
    host_username = models.CharField(max_length=1000)
    host_password = models.CharField(max_length=1000)
    host_email = models.CharField(max_length=1000)
    host_port = models.IntegerField(default=465)
    is_deleted = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_smtp_conf'


class OutgoingEmails(models.Model):
    PENDING = 1
    PROCESSING = 2
    SUCCESS = 3
    DELIVERED = 4
    ERROR = -3
    STATUS_CHOICES_DICT = {'PENDING': 'Pending',  'PROCESSING': 'Processing',
                           'SUCCESS': 'Success',  'DELIVERED': 'Delivered', 'ERROR': 'Error'}
    STATUS_CHOICES = (
        (PENDING, STATUS_CHOICES_DICT.get('PENDING')),
        (PROCESSING, STATUS_CHOICES_DICT.get('PROCESSING')),
        (SUCCESS, STATUS_CHOICES_DICT.get('SUCCESS')),
        (DELIVERED, STATUS_CHOICES_DICT.get('DELIVERED')),
        (ERROR, STATUS_CHOICES_DICT.get('ERROR')))

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)
    to_address = models.TextField()
    cc_address = models.TextField(null=True, blank=True)
    bcc_address = models.TextField(null=True, blank=True)
    from_address = models.EmailField(max_length=250, null=True, blank=True)
    subject = models.CharField(max_length=1000)
    content = models.TextField(null=True, blank=True)
    attached_files = models.CharField(max_length=500, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    queue_time = models.DateTimeField(null=True, blank=True)
    sent_time = models.DateTimeField(null=True, blank=True)
    header_message = models.TextField(null=True, blank=True)
    footer_message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_outgoing_emails'


class EmailToTicketConf(models.Model):
    id = models.AutoField(primary_key=True)
    email_id = models.EmailField(max_length=255)
    password = models.CharField(max_length=128, null=True, blank=True)
    smtp_host_port = models.IntegerField()
    email_server = models.CharField(max_length=255, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_email_to_ticket_conf'


class IncomingEmails(models.Model):
    PENDING = 1
    PROCESSING = 2
    PROCESSED = 3
    ERROR = -3
    STATUS_CHOICES_DICT = {'PENDING': 'Pending',  'PROCESSING': 'Processing',
                           'PROCESSED': 'Processed', 'ERROR': 'Error'}
    STATUS_CHOICES = (
        (PENDING, STATUS_CHOICES_DICT.get('PENDING')),
        (PROCESSING, STATUS_CHOICES_DICT.get('PROCESSING')),
        (PROCESSED, STATUS_CHOICES_DICT.get('PROCESSED')),
        (ERROR, STATUS_CHOICES_DICT.get('ERROR')))

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)
    from_address = models.EmailField(max_length=250, null=True, blank=True)
    subject = models.CharField(max_length=1000)
    content = models.TextField(null=True, blank=True)
    attached_files = models.CharField(max_length=500, blank=True, null=True)
    received_time = models.DateTimeField(null=True, blank=True)
    convert_time = models.DateTimeField(null=True, blank=True)
    is_converted = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_incoming_emails'


class Workflow(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_workflow'


class WorkflowOwners(models.Model):
    id = models.AutoField(primary_key=True)
    wf = models.ForeignKey(Workflow, on_delete=(models.CASCADE))
    owner = models.ForeignKey(User, on_delete=(models.CASCADE))
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_workflow_owners'


class State(models.Model):
    id = models.AutoField(primary_key=True)
    wf = models.ForeignKey(Workflow, on_delete=(models.CASCADE))
    name = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_state'


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    wf = models.ForeignKey(Workflow, on_delete=(models.CASCADE))
    state = models.ForeignKey(State, on_delete=(models.CASCADE))
    name = models.CharField(max_length=255)
    stage = models.CharField(max_length=255, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_status'


class Rules(models.Model):
    id = models.AutoField(primary_key=True)
    wf = models.ForeignKey(Workflow, on_delete=(models.CASCADE))
    is_stage_rule = models.BooleanField(default=False)
    if_state = models.ForeignKey(
        State, related_name='if_state', blank=True, null=True, on_delete=(models.CASCADE))
    if_status = models.ForeignKey(
        Status, related_name='if_status', blank=True, null=True, on_delete=(models.CASCADE))
    if_stage = models.CharField(max_length=255, blank=True, null=True)
    then_state = models.ForeignKey(
        State, related_name='then_state', on_delete=(models.CASCADE))
    then_status = models.ForeignKey(
        Status, related_name='then_status', on_delete=(models.CASCADE))
    name = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_rules'


class Notifications(models.Model):
    id = models.AutoField(primary_key=True)
    wf = models.ForeignKey(Workflow, on_delete=(models.CASCADE))
    is_stage_notification = models.BooleanField(default=False)
    state = models.ForeignKey(State, on_delete=(
        models.CASCADE), blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=(
        models.CASCADE), blank=True, null=True)
    stage = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=1000)
    body = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_notifications'
