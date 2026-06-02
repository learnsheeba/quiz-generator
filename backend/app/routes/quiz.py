from fastapi import APIRouter, HTTPException, status

from app.schemas import (
    CurrentQuestionResponse,
    QuestionPublic,
    StartQuizRequest,
    StartQuizResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.services.question_generator import QuestionGenerationError, generate_questions
from app.services.quiz_store import TOTAL_QUESTIONS, quiz_store


router = APIRouter(prefix="/api/quiz", tags=["quiz"])


def _to_public_question(session) -> QuestionPublic:
    q = session.questions[session.current_index]
    return QuestionPublic(question=q.question, options=q.options)


@router.post("/start", response_model=StartQuizResponse)
def start_quiz(payload: StartQuizRequest) -> StartQuizResponse:
    try:
        questions = generate_questions(payload.topic.strip())
    except QuestionGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    session = quiz_store.create_session(topic=payload.topic.strip(), questions=questions)
    return StartQuizResponse(
        quiz_id=session.quiz_id,
        question=_to_public_question(session),
        current_index=1,
        total=TOTAL_QUESTIONS,
    )


@router.get("/{quiz_id}/current", response_model=CurrentQuestionResponse)
def get_current_question(quiz_id: str) -> CurrentQuestionResponse:
    session = quiz_store.get_session(quiz_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found or expired.")

    if session.current_index >= TOTAL_QUESTIONS:
        return CurrentQuestionResponse(
            done=True,
            current_index=TOTAL_QUESTIONS,
            total=TOTAL_QUESTIONS,
            score=session.score,
        )

    return CurrentQuestionResponse(
        done=False,
        current_index=session.current_index + 1,
        total=TOTAL_QUESTIONS,
        question=_to_public_question(session),
    )


@router.post("/answer", response_model=SubmitAnswerResponse)
def submit_answer(payload: SubmitAnswerRequest) -> SubmitAnswerResponse:
    session = quiz_store.get_session(payload.quiz_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found or expired.")

    if session.current_index >= TOTAL_QUESTIONS:
        return SubmitAnswerResponse(
            done=True,
            current_index=TOTAL_QUESTIONS,
            total=TOTAL_QUESTIONS,
            score=session.score,
        )

    current_question = session.questions[session.current_index]
    if payload.selected_option == current_question.correct_option_index:
        session.score += 1

    session.current_index += 1

    if session.current_index >= TOTAL_QUESTIONS:
        return SubmitAnswerResponse(
            done=True,
            current_index=TOTAL_QUESTIONS,
            total=TOTAL_QUESTIONS,
            score=session.score,
        )

    next_question = session.questions[session.current_index]
    return SubmitAnswerResponse(
        done=False,
        current_index=session.current_index + 1,
        total=TOTAL_QUESTIONS,
        question=QuestionPublic(question=next_question.question, options=next_question.options),
    )
