import React, { useRef, useEffect } from "react";

export default function WebcamCapture({ onCapture }) {
  const videoRef = useRef();

  useEffect(() => {
    async function start() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      } catch (err) {
        console.error("Camera error", err);
      }
    }
    start();
    return () => {
      if(videoRef.current && videoRef.current.srcObject){
        videoRef.current.srcObject.getTracks().forEach(t => t.stop());
      }
    }
  }, []);

  function capture(){
    const video = videoRef.current;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
    onCapture(dataUrl);
  }

  return (
    <div>
      <video ref={videoRef} style={{ width: "100%", maxWidth: 420 }} autoPlay muted />
      <div>
        <button onClick={capture}>Capture</button>
      </div>
    </div>
  );
}
