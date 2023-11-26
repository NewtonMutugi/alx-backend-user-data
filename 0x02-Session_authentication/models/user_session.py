#!/usr/bin/env python3
"""User Session Module"""
from .base import Base


class UserSession(Base):
    """UserSession class inherits from Base"""

    def __init__(self, *args: list, **kwargs: dict):
        """initializes UserSession"""
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
