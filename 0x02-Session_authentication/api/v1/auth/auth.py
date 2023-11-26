#!/usr/bin/env python3
"""Authentication module for the API."""
import re
from typing import List, TypeVar
from os import getenv


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Confirms whether required path needs authorization"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded in excluded_paths:
            regex = re.compile(excluded.replace('*', '.*?'))
            if regex.match(path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header field from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user from the request."""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        SESSION_NAME = getenv("SESSION_NAME")

        if SESSION_NAME is None:
            return None
        return request.cookies.get(SESSION_NAME)
