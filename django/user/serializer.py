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
    role_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'last_login', 'is_active', 'profile', 'role_id')

    def get_profile(self, obj):
        try:
            profile = self.context.get('prof_data', {})
            return profile
        except Exception as err:
            return {}

    def get_role_id(self, obj):
        try:
            role_id = self.context.get('role_id', '')
            return role_id
        except Exception as err:
            return None


class CustomerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'email')


class CustomerDataSerializer(serializers.ModelSerializer):
    image_data = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(
        source='user.last_login', format=DATE_TIME_FORMAT, read_only=True, allow_null=True)
    username = serializers.CharField(
        source='user.username', allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(
        source='user.is_active', read_only=True, allow_null=True)

    class Meta:
        model = Customer
        fields = ('id', 'email', 'image_data', 'customer_name', 'login_enabled',
                  'profile_path', 'contact_number', 'username', 'last_login', 'is_active')

    def get_image_data(self, obj):
        try:
            image_path = obj.profile_path
            with open(image_path, "rb") as img_file:
                b64str = base64.b64encode(img_file.read())
            return 'data:image/jpeg;base64,' + b64str.decode('utf-8')
        except Exception as err:
            return ''
