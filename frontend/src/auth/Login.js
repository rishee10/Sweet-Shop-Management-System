import sweetImg from "../assets/image1.png";

import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const login = async () => {
    try {
      const res = await api.post("auth/login/", form);

      // Original logic: decode JWT to get role
      const token = res.data.access;
      localStorage.setItem("token", token);

      const payload = JSON.parse(atob(token.split(".")[1]));
      const role = payload.is_staff ? "admin" : "user";
      localStorage.setItem("role", role);

      navigate(role === "admin" ? "/admin" : "/user");
    } catch {
      alert("Invalid credentials");
    }
  };

  return (

    <div className="auth-container">
      <div className="auth-left">
          <img
    src={sweetImg}
    alt="image1"
    style={{
      width: "220px",
      marginBottom: "30px"
    }}
  />

        <h1>🍭 Sweet Delights</h1>
        <p>
          Experience authentic Indian sweets made with love, tradition,
          and premium ingredients.
        </p>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <h2>Welcome Back</h2>

          <input
            className="input"
            placeholder="Username"
            value={form.username}
            onChange={(e) =>
              setForm({ ...form, username: e.target.value })
            }
          />

          <input
            className="input"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />

          <button className="button" onClick={login}>
            Login
          </button>

          <div className="auth-footer">
            New here?{" "}
            <span onClick={() => navigate("/register")}>
              Create an account
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
