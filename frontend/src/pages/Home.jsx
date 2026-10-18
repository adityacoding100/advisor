import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../Home.css";
function Home() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");

  const openChat = (event) => {
    event.preventDefault();
    const trimmedQuestion = question.trim();
    if (trimmedQuestion) {
      navigate("/chat", { state: { question: trimmedQuestion } });
    }
  };

  return (
    <div className="home-page">
      <header className="navbar">
        <Link className="logo" to="/">FinAdvisor</Link>
        <nav className="nav-links" aria-label="Account navigation">
          <Link to="/login">Login</Link>
        </nav>
      </header>

      <main className="home-main">
        <section className="home-content" aria-labelledby="home-title">
          <p className="home-eyebrow">FinAdvisor</p>
          <h1 className="home-title" id="home-title">
            What would you like to understand?
          </h1>
          <p className="home-description">
            Ask a question about your financial documents to start a conversation.
          </p>

          <form className="home-question-form" onSubmit={openChat}>
            <input
              id="home-question"
              aria-label="Ask your financial question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask your financial question..."
            />
            <button type="submit" disabled={!question.trim()}>
              Open chat
            </button>
          </form>
          <p className="home-note">For educational purposes only. Not personal financial advice.</p>
        </section>
      </main>

      <footer className="home-footer">
        © 2026 FinAdvisor
      </footer>
    </div>
  );
}

export default Home;