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

      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">
          FinAdvisor
        </div>

        <div className="nav-links">
          <Link to="/login">Login</Link>
          <Link to="/register" className="register-btn">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="hero">

        <div className="hero-content">
          <span className="badge">
            AI-Powered Financial Assistant
          </span>

          <h1>
            Understand your finances
            <span> with AI.</span>
          </h1>

          <p>
            Ask questions about investments, markets, financial concepts,
            and your portfolio. Get intelligent answers powered by
            AI and your trusted financial documents.
          </p>

          <div className="hero-buttons">
            <Link to="/register" className="primary-btn">
              Start for Free
            </Link>

            <Link to="/login" className="secondary-btn">
              Login
            </Link>
          </div>
        </div>

        {/* Chat Preview */}
        <div className="chat-preview">

          <div className="chat-header">
            <div className="bot-icon">AI</div>

            <div>
              <strong>Financial Advisor</strong>
              <small>Online</small>
            </div>
          </div>

          <div className="message user-message">
            Should I invest in technology stocks?
          </div>

          <div className="message bot-message">
            Technology stocks can offer strong growth potential,
            but they may also have higher volatility. Your decision
            should consider your investment horizon, risk tolerance,
            and portfolio diversification.
          </div>

          <form className="chat-input" onSubmit={openChat}>
            <input
              aria-label="Ask your financial question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask your financial question..."
            />
            <button type="submit" disabled={!question.trim()}>
              Ask
            </button>
          </form>

        </div>

      </main>

      {/* Features */}
      <section className="features">

        <div className="feature-card">
          <div className="feature-icon">🤖</div>
          <h3>AI-Powered Advice</h3>
          <p>
            Get contextual answers using modern LLM technology.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">📚</div>
          <h3>RAG Knowledge</h3>
          <p>
            Retrieve relevant information from trusted financial documents.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">💬</div>
          <h3>Natural Conversations</h3>
          <p>
            Ask financial questions using simple natural language.
          </p>
        </div>

      </section>

      {/* Footer */}
      <footer>
        <p>
          © 2026 FinAdvisor. For educational purposes only.
        </p>
      </footer>

    </div>
  );
}

export default Home;