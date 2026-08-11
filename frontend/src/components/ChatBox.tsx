import { useState } from "react";
import ReactMarkdown from "react-markdown";

import { api } from "../api";
import type { ChatMessage } from "../types";
import PalCardLink from "./PalCardLink";


type Props = {
  messages: ChatMessage[];
  setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  sessionId: string | null;
  setSessionId: (value: string | null) => void;
};


const suggestions = [
  "前期基地最值得抓谁？",
  "火绒狐和燎火鹿怎么选？",
  "谁适合浇水和搬运？",
];


function ChatBox({ messages, setMessages, sessionId, setSessionId }: Props) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(nextQuestion = question) {
    const trimmed = nextQuestion.trim();
    if (!trimmed || loading) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmed,
    };

    setMessages((current) => [...current, userMessage]);
    setQuestion("");
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/ask", {
        question: trimmed,
        session_id: sessionId,
      });
      setSessionId(response.data.session_id);
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: response.data.answer,
          sources: response.data.sources,
        },
      ]);
    } catch {
      setError("问答服务暂时不可用，请确认后端、向量库和 API 配置已就绪。");
    } finally {
      setLoading(false);
    }
  }

  async function clearConversation() {
    if (sessionId) {
      try {
        await api.delete(`/sessions/${sessionId}`);
      } catch {
        // Local history should still be clearable when the backend is offline.
      }
    }
    setMessages([]);
    setSessionId(null);
    setError("");
  }

  return (
    <section className="chat-shell" aria-label="帕鲁 AI 问答">
      <div className="chat-header">
        <div>
          <span className="eyebrow">RAG GUIDE</span>
          <h2>问问帕鲁助手</h2>
          <p>支持连续追问，会结合最近的对话理解你的问题。</p>
        </div>
        {messages.length > 0 && (
          <button className="text-button" onClick={clearConversation}>新对话</button>
        )}
      </div>

      <div className="chat-history" aria-live="polite">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <div className="assistant-orb">AI</div>
            <strong>从培养、工作、属性或掉落开始问</strong>
            <div className="suggestion-list">
              {suggestions.map((suggestion) => (
                <button key={suggestion} onClick={() => handleSubmit(suggestion)}>
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div className={`message-row ${message.role}`} key={message.id}>
              <div className="message-bubble">
                {message.role === "assistant" ? (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                ) : (
                  <p>{message.content}</p>
                )}
                {message.sources && message.sources.length > 0 && (
                  <div className="source-list">
                    <span>参考帕鲁</span>
                    {message.sources.map((source) => (
                      <PalCardLink key={source.name} source={source} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message-row assistant">
            <div className="message-bubble typing"><i /><i /><i /></div>
          </div>
        )}
      </div>

      {error && <p className="chat-error">{error}</p>}

      <form
        className="chat-composer"
        onSubmit={(event) => {
          event.preventDefault();
          void handleSubmit();
        }}
      >
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder={messages.length ? "继续追问，例如：那和企丸丸相比呢？" : "输入你的帕鲁问题…"}
          maxLength={1000}
        />
        <button type="submit" disabled={!question.trim() || loading}>
          {loading ? "思考中" : "发送"}
        </button>
      </form>
    </section>
  );
}


export default ChatBox;
