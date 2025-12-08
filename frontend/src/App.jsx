import React from "react";
import { Outlet } from "react-router-dom";
import NavBar from "./components/NavBar";

export default function App() {
  return (
    <div>
      <NavBar />
      <main style={{ padding: 20 }}>
        <Outlet />
      </main>
    </div>
  );
}
