#!/usr/bin/env python3
""" Module of Session in Database
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session in database Class"""

    def create_session(self, user_id=None):
        """Create session in database"""
        session_id = super().create_session(user_id)

        if session_id is not None:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get User ID for Session ID from the database"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})

        if user_sessions:
            user_session = user_sessions[0]
            expired_time = user_session.created_at + \
                timedelta(seconds=self.session_duration)

            if expired_time >= datetime.utcnow():
                return user_session.user_id

        return None

    def destroy_session(self, request=None):
        """Remove Session from Database"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if user_id:
            user_sessions = UserSession.search({'session_id': session_id})

            if user_sessions:
                user_session = user_sessions[0]

                try:
                    user_session.remove()
                    UserSession.save_to_file()
                except Exception:
                    return False
                else:
                    return True

        return False
