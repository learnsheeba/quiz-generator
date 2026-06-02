export type Question = {
  question: string;
  options: string[];
};

export type StartQuizResponse = {
  quiz_id: string;
  question: Question;
  current_index: number;
  total: number;
};

export type CurrentQuestionResponse = {
  done: boolean;
  question?: Question;
  current_index: number;
  total: number;
  score?: number;
};

export type SubmitAnswerResponse = {
  done: boolean;
  question?: Question;
  current_index: number;
  total: number;
  score?: number;
};
