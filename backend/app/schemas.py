from typing import List, Optional

from pydantic import BaseModel, Field


class QuestionPublic(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)


class StartQuizRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=120)


class StartQuizResponse(BaseModel):
    quiz_id: str
    question: QuestionPublic
    current_index: int
    total: int = 10


class SubmitAnswerRequest(BaseModel):
    quiz_id: str
    selected_option: int = Field(ge=0, le=3)


class SubmitAnswerResponse(BaseModel):
    done: bool
    current_index: int
    total: int = 10
    question: Optional[QuestionPublic] = None
    score: Optional[int] = None


class CurrentQuestionResponse(BaseModel):
    done: bool
    current_index: int
    total: int = 10
    question: Optional[QuestionPublic] = None
    score: Optional[int] = None
