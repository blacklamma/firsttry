from django.db import models
from django.contrib.auth.models import User


class Tickets(models.Model):
    display_id = models.CharField(max_length=30)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    customer = models.CharField(blank=True, null=True)  # fkey
    summary = models.CharField(blank=True, null=True, max_length=10000)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    workflow_config = models.CharField(blank=True, null=True)  # fkey
    service_category = models.CharField(blank=True, null=True)  # fkey
    impact_service = models.CharField(blank=True, null=True)  # fkey
    service_classification = models.CharField(blank=True, null=True)  # fkey
    state = models.CharField(blank=True, null=True)  # fkey
    status = models.CharField(blank=True, null=True)  # fkey
    impact = models.SmallIntegerField(default=1)
    urgency = models.SmallIntegerField(default=1)
    priority = models.SmallIntegerField(default=1)
    group = models.CharField(blank=True, null=True)  # fkey
    level = models.CharField(blank=True, null=True)  # fkey
    assignee = models.ForeignKey(
        User, null=True, blank=True, related_name='incident_assignee', on_delete=(models.CASCADE))
    source = models.SmallIntegerField(default=1)
    resolution_type = models.CharField(max_length=30, null=True, blank=True)
    resolutionTime = models.CharField(max_length=30, null=True, blank=True)
    symptom = models.TextField(null=True, blank=True)
    root_cause = models.TextField(null=True, blank=True)
    resolution = models.TextField(null=True, blank=True)
    trouble_reason = models.TextField(null=True, blank=True)
    recovery_action = models.TextField(null=True, blank=True)
    closure_note = models.TextField(null=True, blank=True)
    closed_by = models.ForeignKey(
        User, null=True, blank=True, related_name='incident_closed_by', on_delete=(models.CASCADE))
    closed_type = models.CharField(max_length=30, null=True, blank=True)
    agreed_closure_date = models.DateTimeField(null=True, blank=True)
    actual_closure_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, related_name='incident_created_by', on_delete=(models.CASCADE))
    person_name = models.CharField(max_length=255, blank=True, null=True)
    person_email = models.TextField(blank=True, null=True)
    person_phone = models.TextField(blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'create', 'change', 'delete')
        db_table = 'tbl_tickets'
