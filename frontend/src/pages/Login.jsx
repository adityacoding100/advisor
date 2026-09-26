import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../Auth.css";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // Later connect this to FastAPI.
    console.log({
      email,
      password
    });

    navigate("/chat");
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          FinAdvisor
        </div>

        <h1>Welcome back</h1>

        <p className="auth-subtitle">
          Login to your financial assistant.
        </p>

        <form onSubmit={handleSubmit}>

          <label>Email</label>

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>

          <input
            type="password"
            placeholder="Your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit">
            Login
          </button>

        </form>

        <p className="auth-footer">
          Don't have an account?{" "}
          <Link to="/register">
            Create one
          </Link>
        </p>

        <Link to="/" className="back-home">
          ← Back to home
        </Link>

      </div>

    </div>
  );
}

export default Login;