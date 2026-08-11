import { useEffect, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Home from "./pages/Home";
import PalDetail from "./pages/PalDetail";
import type { ChatMessage } from "./types";


const MESSAGES_KEY = "my-pal-ai:messages";
const SESSION_KEY = "my-pal-ai:session";


function loadMessages(): ChatMessage[] {
  try {
    return JSON.parse(localStorage.getItem(MESSAGES_KEY) ?? "[]") as ChatMessage[];
  } catch {
    return [];
  }
}


function App() {
  const [messages, setMessages] = useState<ChatMessage[]>(loadMessages);
  const [sessionId, setSessionId] = useState<string | null>(() =>
    localStorage.getItem(SESSION_KEY),
  );

  useEffect(() => {
    localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    if (sessionId) {
      localStorage.setItem(SESSION_KEY, sessionId);
    } else {
      localStorage.removeItem(SESSION_KEY);
    }
  }, [sessionId]);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Home
              messages={messages}
              setMessages={setMessages}
              sessionId={sessionId}
              setSessionId={setSessionId}
            />
          }
        />
        <Route path="/pal/:name" element={<PalDetail />} />
      </Routes>
    </BrowserRouter>
  );
}


export default App;
