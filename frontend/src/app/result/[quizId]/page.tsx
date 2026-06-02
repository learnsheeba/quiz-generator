"use client";

import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";

export default function ResultPage() {
  const params = useParams<{ quizId: string }>();
  const searchParams = useSearchParams();

  const score = Number(searchParams.get("score") || 0);
  const total = Number(searchParams.get("total") || 10);
  const percentage = total > 0 ? Math.round((score / total) * 100) : 0;

  return (
    <main>
      <div className="card stack">
        <h1>Quiz Complete</h1>
        <p>
          Quiz ID: <code>{params.quizId}</code>
        </p>
        <h2>
          Score: {score} / {total}
        </h2>
        <p>{percentage}% correct</p>
        <Link className="button" href="/">
          Try Another Topic
        </Link>
      </div>
    </main>
  );
}
