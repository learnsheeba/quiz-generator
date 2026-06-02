"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { startQuiz } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onStart = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    if (!topic.trim()) {
      setError("Please enter a topic.");
      return;
    }

    try {
      setLoading(true);
      const response = await startQuiz(topic.trim());
      router.push(`/quiz/${response.quiz_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start quiz.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <div className="card stack">
        <h1>Quiz Generator</h1>
        <p>Enter any topic and answer 10 generated questions.</p>
        <form className="stack" onSubmit={onStart}>
          <input
            className="input"
            type="text"
            value={topic}
            onChange={(event) => setTopic(event.target.value)}
            placeholder="e.g. JavaScript basics"
          />
          <button className="button" type="submit" disabled={loading}>
            {loading ? "Generating quiz..." : "Start Quiz"}
          </button>
        </form>
        {error ? <p className="error">{error}</p> : null}
      </div>
    </main>
  );
}
