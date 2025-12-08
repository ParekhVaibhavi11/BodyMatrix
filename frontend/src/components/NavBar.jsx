import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function NavBar(){
  const nav = useNavigate();
  const logout = () => {
    localStorage.removeItem("token");
    nav("/auth");
  };
  return (
    <nav>
      <Link to="/">BodyMatrix</Link>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/new-scan">New Scan</Link>
      <Link to="/history">History</Link>
      <Link to="/profile">Profile</Link>
      <button onClick={logout} style={{ float: "right" }}>Logout</button>
    </nav>
  )
}
