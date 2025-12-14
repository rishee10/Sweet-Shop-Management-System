import sweetImg from "../assets/image1.png";
import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    confirm_password: "",
  });

  const navigate = useNavigate();

  const register = async () => {
    if (form.password !== form.confirm_password) {
      alert("Passwords do not match");
      return;
    }

    try {
      await api.post("auth/register/", {
        username: form.username,
        password: form.password,
      });
      alert("Registration successful");
      navigate("/");
    } catch {
      alert("Registration failed");
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
        <h1>🍬 Join Sweet Delights</h1>
        <p>
          Create an account and enjoy our delicious collection of sweets.
        </p>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <h2>Create Account</h2>

          <input
            className="input"
            placeholder="Username"
            onChange={(e) =>
              setForm({ ...form, username: e.target.value })
            }
          />

          <input
            className="input"
            type="password"
            placeholder="Password"
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />

          <input
            className="input"
            type="password"
            placeholder="Confirm Password"
            onChange={(e) =>
              setForm({ ...form, confirm_password: e.target.value })
            }
          />

          <button className="button" onClick={register}>
            Register
          </button>

          <div className="auth-footer">
            Already have an account?{" "}
            <span onClick={() => navigate("/")}>
              Login
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

