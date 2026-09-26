import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../Auth.css";

function Register() {

  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (formData.password.length < 8) {
      setError("Password must contain at least 8 characters.");
      return;
    }

    // Later we will replace this with FastAPI API call.
    console.log("Registration data:", formData);

    navigate("/login");
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          FinAdvisor
        </div>

        <h1>Create your account</h1>

        <p className="auth-subtitle">
          Start using your AI financial assistant.
        </p>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>

          <label>Name</label>

          <input
            type="text"
            name="name"
            placeholder="Enter your name"
            value={formData.name}
            onChange={handleChange}
            required
          />

          <label>Email</label>

          <input
            type="email"
            name="email"
            placeholder="you@example.com"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <label>Password</label>

          <input
            type="password"
            name="password"
            placeholder="Create a password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <label>Confirm Password</label>

          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm your password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />

          <button type="submit">
            Create Account
          </button>

        </form>

        <p className="auth-footer">
          Already have an account?{" "}
          <Link to="/login">
            Login
          </Link>
        </p>

        <Link to="/" className="back-home">
          ← Back to home
        </Link>

      </div>

    </div>
  );
}

export default Register;