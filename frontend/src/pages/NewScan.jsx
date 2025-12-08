import React, { useState } from "react";
import WebcamCapture from "../components/WebcamCapture";
import { apiPost } from "../api/api";

export default function NewScan(){
  const [mode, setMode] = useState("body"); // or 'face'
  const [result, setResult] = useState(null);

  async function handleCapture(dataUrl){
    setResult({ status: "uploading" });
    const res = await apiPost("/api/scan", { type: mode, image: dataUrl });
    setResult(res);
  }

  return (
    <div>
      <h2>New Scan</h2>
      <div>
        <button onClick={() => setMode("body")} style={{ fontWeight: mode==="body"? "bold":"normal" }}>Body</button>
        <button onClick={() => setMode("face")} style={{ fontWeight: mode==="face"? "bold":"normal" }}>Face</button>
      </div>
      <p>Mode: {mode}</p>
      <WebcamCapture onCapture={handleCapture} />
      <div>
        <h3>Result</h3>
        <pre style={{ whiteSpace: "pre-wrap" }}>
          {result ? JSON.stringify(result, null, 2) : "No result yet"}
        </pre>
      </div>
    </div>
  )
}
