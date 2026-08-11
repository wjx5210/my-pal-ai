export type Source = {
  name: string;
  type: "entity" | "semantic";
  url: string;
  score?: number | null;
};

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export type CombatInfo = {
  positioning: string;
  strengths: string[];
  weaknesses: string[];
};

export type Pal = {
  name: string;
  element: string[];
  summary: string;
  work_suitability: Record<string, number>;
  combat: CombatInfo;
  drops: string[];
  locations: string[];
  recommended_stage: string;
  recommendation: string;
  tips: string;
};
