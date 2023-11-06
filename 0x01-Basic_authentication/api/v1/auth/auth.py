#!/usr/bin/env python3
"""Authorization module for API"""
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth method
        return: boolean value
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header method
        return: string or None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current User method
        return: User or None"""
        return None
