from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Dict, List
from uuid import uuid4


TOTAL_QUESTIONS = 10
SESSION_TTL_MINUTES = 30


@dataclass
class StoredQuestion:
    question: str
    options: List[str]
    correct_option_index: int


@dataclass
class QuizSession:
    quiz_id: str
    topic: str
    questions: List[StoredQuestion]
    current_index: int
    score: int
    created_at: datetime
    updated_at: datetime


class QuizStore:
    def __init__(self) -> None:
        self._sessions: Dict[str, QuizSession] = {}
        self._lock = Lock()

    def create_session(self, topic: str, questions: List[StoredQuestion]) -> QuizSession:
        if len(questions) != TOTAL_QUESTIONS:
            raise ValueError("Expected exactly 10 questions.")

        now = datetime.now(timezone.utc)
        quiz_id = str(uuid4())
        session = QuizSession(
            quiz_id=quiz_id,
            topic=topic,
            questions=questions,
            current_index=0,
            score=0,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._cleanup_expired_locked(now)
            self._sessions[quiz_id] = session
        return session

    def get_session(self, quiz_id: str) -> QuizSession | None:
        now = datetime.now(timezone.utc)
        with self._lock:
            self._cleanup_expired_locked(now)
            session = self._sessions.get(quiz_id)
            if session:
                session.updated_at = now
            return session

    def _cleanup_expired_locked(self, now: datetime) -> None:
        cutoff = now - timedelta(minutes=SESSION_TTL_MINUTES)
        expired_ids = [sid for sid, s in self._sessions.items() if s.updated_at < cutoff]
        for sid in expired_ids:
            self._sessions.pop(sid, None)


quiz_store = QuizStore()
