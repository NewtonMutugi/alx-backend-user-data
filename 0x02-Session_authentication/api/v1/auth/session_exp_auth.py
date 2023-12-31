#!/usr/bin/env python3
"""Session Expiration Authentication"""
from datetime import datetime, timedelta
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Adds an expiration date to a Session ID."""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            session_duration = int(SESSION_DURATION)
        except (ValueError, TypeError):
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""

        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None or self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')

        if created_at is None:
            return None

        created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        expired_time = created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        return session_dictionary.get('user_id')
