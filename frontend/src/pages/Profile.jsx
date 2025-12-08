// Dashboard.jsx
import React, { useEffect, useState } from "react";
import { apiGet } from "../api/api";
export default function Dashboard(){
  const [latest, setLatest] = useState(null);
  useEffect(()=>{ apiGet("/api/measurements/latest").then(setLatest) }, []);
  return (
    <div>
      <h2>Dashboard</h2>
      <pre>{ latest ? JSON.stringify(latest, null, 2) : "Loading..." }</pre>
    </div>
  )
}
