# Quiz Generator (Next.js + FastAPI)

```
<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/f0a33024d25143bfafde028b37fd0389" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>
```

This project generates a 10-question quiz from a user-provided topic using OpenAI `gpt-4o`.

- Questions are generated in one OpenAI call at quiz start.
- Questions are shown one-by-one in the frontend.
- Score is calculated server-side and shown on the final page.

## Project Structure

- `frontend/` - Next.js app (App Router, TypeScript)
- `backend/` - FastAPI app

## Backend Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Copy env file and set your API key:

   ```bash
   cp backend/.env.example backend/.env
   ```

4. Run backend:

   ```bash
   uvicorn backend.main:app --reload
   ```

Backend runs on `http://localhost:8000`.

## Frontend Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Copy env file:

   ```bash
   cp .env.local.example .env.local
   ```

3. Run frontend:

   ```bash
   npm run dev
   ```

Frontend runs on `http://localhost:3000`.

## API Endpoints

- `POST /api/quiz/start`  
  Body: `{ "topic": "string" }`  
  Returns quiz ID + question 1.

- `GET /api/quiz/{quiz_id}/current`  
  Returns current question for the session, or final score if already complete.

- `POST /api/quiz/answer`  
  Body: `{ "quiz_id": "uuid", "selected_option": 0..3 }`  
  Returns next question or final score after question 10.

## Error Handling

- Invalid or expired quiz ID returns `404`.
- Invalid OpenAI output is retried once; if still invalid, API returns `502`.
- Missing/invalid topic returns validation errors from FastAPI.
