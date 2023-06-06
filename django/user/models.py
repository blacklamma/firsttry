from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=(models.CASCADE))
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    profile_path = models.CharField(max_length=500, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    contact_extension = models.CharField(max_length=15, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        default_permissions = ('view', 'create', 'change', 'delete')
        db_table = 'tbl_user_profile'
