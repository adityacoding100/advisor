
import { useCallback, useEffect, useRef, useState } from "react";
import axios from "axios";
import { Link, useLocation } from "react-router-dom";
import "../Chat.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

function Chat() {
  const location = useLocation();
  const initialQuestion = useRef(location.state?.question ?? "");
  const [message, setMessage] = useState(location.state?.question ?? "");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Ask a question about your financial documents to get started.",
    },
  ]);
  const [isSending, setIsSending] = useState(false);

  const sendQuestion = useCallback(async (question) => {
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || isSending) return;

    setMessages((previous) => [...previous, { role: "user", text: trimmedQuestion }]);
    setMessage("");
    setIsSending(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        message: trimmedQuestion,
      });
      const answer = response.data?.candidates?.[0]?.content?.parts
        ?.map((part) => part.text ?? "")
        .join("\n");

      if (!answer) {
        throw new Error("The chat service returned an empty response.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: answer,
          sources: response.data.sources ?? [],
        },
      ]);
    } catch (error) {
      console.error(error);
      const detail = error.response?.data?.detail;
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: typeof detail === "string"
            ? detail
            : "Could not reach the chat service. Check that the backend is running and try again.",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  }, [isSending]);

  useEffect(() => {
    const question = initialQuestion.current;
    if (!question) return;

    initialQuestion.current = "";
    void sendQuestion(question);
  }, [sendQuestion]);

  const sendMessage = async (event) => {
    event.preventDefault();
    const question = message.trim();
    if (!question || isSending) return;
    await sendQuestion(question);
  };

  return (
    <main className="chat-page">
      <header className="chat-page-header">
        <Link className="chat-brand" to="/">FinAdvisor</Link>
        <span className="chat-status"><span /> Gemini financial assistant</span>
      </header>

      <section className="conversation" aria-live="polite" aria-label="Conversation">
        {messages.map((item, index) => (
          <article className={`chat-message ${item.role}`} key={`${item.role}-${index}`}>
            <span className="message-author">
              {item.role === "user" ? "You" : "FinAdvisor"}
            </span>
            <p>{item.text}</p>
            {item.sources?.length > 0 && (
              <small className="message-sources">
                Sources: {item.sources.map((source) =>
                  `${source.file}${source.page ? `, p. ${source.page}` : ""}`
                ).join("; ")}
              </small>
            )}
          </article>
        ))}
        {isSending && <p className="chat-loading">Reviewing your documents...</p>}
      </section>

      <form className="chat-composer" onSubmit={sendMessage}>
        <textarea
          aria-label="Ask your financial question"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              event.currentTarget.form.requestSubmit();
            }
          }}
          placeholder="Ask your financial question..."
          rows={2}
          disabled={isSending}
        />
        <button type="submit" disabled={!message.trim() || isSending}>
          {isSending ? "Sending..." : "Send"}
        </button>
      </form>
      <p className="chat-disclaimer">For educational purposes only. Not personal financial advice.</p>
    </main>
  );
}

export default Chat;