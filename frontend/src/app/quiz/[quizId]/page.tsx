"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { getCurrentQuestion, submitAnswer } from "@/lib/api";
import type { Question } from "@/types/quiz";

export default function QuizPage() {
  const params = useParams<{ quizId: string }>();
  const router = useRouter();
  const quizId = useMemo(() => params?.quizId ?? "", [params]);

  const [question, setQuestion] = useState<Question | null>(null);
  const [currentIndex, setCurrentIndex] = useState(1);
  const [total, setTotal] = useState(10);
  const [selected, setSelected] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const run = async () => {
      if (!quizId) {
        return;
      }
      try {
        setLoading(true);
        const response = await getCurrentQuestion(quizId);
        if (response.done) {
          router.replace(`/result/${quizId}?score=${response.score ?? 0}&total=${response.total}`);
          return;
        }
        setQuestion(response.question || null);
        setCurrentIndex(response.current_index);
        setTotal(response.total);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load question.");
      } finally {
        setLoading(false);
      }
    };

    run();
  }, [quizId, router]);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    if (selected === null) {
      setError("Please choose an option.");
      return;
    }

    try {
      setSubmitting(true);
      const response = await submitAnswer(quizId, selected);
      if (response.done) {
        router.replace(`/result/${quizId}?score=${response.score ?? 0}&total=${response.total}`);
        return;
      }
      setQuestion(response.question || null);
      setCurrentIndex(response.current_index);
      setTotal(response.total);
      setSelected(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <main>
        <div className="card">Loading quiz...</div>
      </main>
    );
  }

  if (!question) {
    return (
      <main>
        <div className="card">
          <p className="error">{error || "Question not available."}</p>
        </div>
      </main>
    );
  }

  return (
    <main>
      <div className="card stack">
        <h2>
          Question {currentIndex} / {total}
        </h2>
        <p>{question.question}</p>
        <form className="stack" onSubmit={onSubmit}>
          {question.options.map((option, idx) => (
            <label key={idx} className="option">
              <input
                type="radio"
                name="answer"
                checked={selected === idx}
                onChange={() => setSelected(idx)}
              />
              <span>{option}</span>
            </label>
          ))}
          <button className="button" type="submit" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Answer"}
          </button>
        </form>
        {error ? <p className="error">{error}</p> : null}
      </div>
    </main>
  );
}
