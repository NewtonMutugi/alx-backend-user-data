#!/usr/bin/env python3
"""Session Expiration Authentication"""
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Adds an expiration date to a Session ID."""

    def __init__(self) -> None:
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        self.session_duration = int(session_duration)

    def create_session(self, user_id=None):
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': self.session_duration
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if 'created_at' not in session_dictionary.keys():
            return None

        if 'user_id' not in session_dictionary.keys():
            return None

        if session_dictionary.get('created_at') < 0:
            return None

        return session_dictionary.get('user_id')
