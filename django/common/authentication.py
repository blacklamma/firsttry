import jwt
from calendar import timegm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.core import signing
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class BaseJSONTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        try:
            api_user_id = None
            jwt_value, user_id = self.get_jwt_value(request)
            if jwt_value is None:
                return None
            try:
                payload = jwt_decode_handler(jwt_value)
            except jwt.ExpiredSignature:
                msg = 'Signature has expired.'
                raise exceptions.AuthenticationFailed(msg)
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed()
            user = self.authenticate_credentials(payload, request)

            return (user, jwt_value)
        except Exception as err:
            print("Method authenticate on Authentication :%s (%s)" %
                  (err, type(err)))

    def authenticate_credentials(self, payload, request):
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = 'Invalid payload.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = 'Invalid signature.'
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = 'User account is disabled.'
            raise exceptions.AuthenticationFailed(msg)
        request.user = user
        return user


class JWTTokenAuthentication(BaseJSONTokenAuthentication):
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or auth[0].lower() != auth_header_prefix:
            return None, None

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        return auth[1], None

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
