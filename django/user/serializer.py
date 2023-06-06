import base64
from backend.config import DATE_TIME_FORMAT
from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(
        format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    is_active_str = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'last_login', 'is_active_str')

    def get_is_active_str(self, obj):
        try:
            if obj.is_active:
                return 'Yes'
            else:
                return 'No'
        except Exception as err:
            return 'No'


class UserProfileDataSerializer(serializers.ModelSerializer):
    image_data = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('department', 'designation', 'profile_path',
                  'image_data', 'contact_number')

    def get_image_data(self, obj):
        try:
            image_path = obj.profile_path
            with open(image_path, "rb") as img_file:
                b64str = base64.b64encode(img_file.read())
            return 'data:image/jpeg;base64,' + b64str.decode('utf-8')
        except Exception as err:
            return ''


class UserDataSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'last_login', 'is_active', 'profile')

    def get_profile(self, obj):
        try:
            profile = self.context.get('prof_data', {})
            return profile
        except Exception as err:
            return {}
