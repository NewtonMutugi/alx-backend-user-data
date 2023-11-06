#!/usr/bin/env python3
"""Authentication module for the API."""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Confirms whether required path needs authorization"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header field from the request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user from the request."""
        return None
