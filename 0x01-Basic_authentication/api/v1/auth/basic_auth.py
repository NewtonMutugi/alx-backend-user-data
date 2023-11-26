#!/usr/bin/env python3
"""Basic authentication module for the API."""

from base64 import b64decode
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """Decodes a Base64 string."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """

        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        split_creds = decoded_base64_authorization_header.split(':', 1)
        return (split_creds[0], split_creds[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            b64_auth_header)
        if decoded_auth_header is None:
            return None
        user_creds = self.extract_user_credentials(decoded_auth_header)
        if user_creds is None:
            return None
        user = self.user_object_from_credentials(user_creds[0], user_creds[1])
        return user
