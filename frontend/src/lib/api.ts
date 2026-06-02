import type {
  CurrentQuestionResponse,
  StartQuizResponse,
  SubmitAnswerResponse
} from "@/types/quiz";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {})
    },
    cache: "no-store"
  });

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail || "Request failed.");
  }
  return data as T;
}

export function startQuiz(topic: string): Promise<StartQuizResponse> {
  return fetchJson<StartQuizResponse>("/api/quiz/start", {
    method: "POST",
    body: JSON.stringify({ topic })
  });
}

export function getCurrentQuestion(quizId: string): Promise<CurrentQuestionResponse> {
  return fetchJson<CurrentQuestionResponse>(`/api/quiz/${quizId}/current`);
}

export function submitAnswer(
  quizId: string,
  selectedOption: number
): Promise<SubmitAnswerResponse> {
  return fetchJson<SubmitAnswerResponse>("/api/quiz/answer", {
    method: "POST",
    body: JSON.stringify({ quiz_id: quizId, selected_option: selectedOption })
  });
}
