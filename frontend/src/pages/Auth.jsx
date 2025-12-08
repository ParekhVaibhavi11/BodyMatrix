import React, { useState } from "react";
import { apiPost } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Auth(){
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const nav = useNavigate();

  async function login(e){
    e.preventDefault();
    const res = await apiPost("/api/auth/login", { email, password });
    if(res.token){
      localStorage.setItem("token", res.token);
      nav("/dashboard");
    } else alert(res.detail || "Login failed");
  }

  async function signup(e){
    e.preventDefault();
    const res = await apiPost("/api/auth/register", { email, password });
    if(res.ok) alert("Registered. Please login.");
    else alert(res.detail || "Register failed");
  }

  return (
    <div>
      <h2>Login / Register</h2>
      <form onSubmit={login}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} type="password" />
        <button type="submit">Login</button>
      </form>
      <button onClick={signup}>Register</button>
    </div>
  )
}
