from fastapi import APIRouter, Depends, HTTPException
import base64, uuid, os
from ..models import ScanIn
from ..services.mediapipe_processor import process_image_for_body
from ..db import measurements_col
from datetime import datetime

router = APIRouter(prefix="/api")

@router.post("/scan")
async def scan_image(payload: dict, user=Depends(lambda: None)):
    # payload expects { type, image }
    t = payload.get("type")
    dataurl = payload.get("image")
    if not t or not dataurl:
        raise HTTPException(400, "Missing fields")
    header, data = dataurl.split(",",1)
    ext = "jpg"
    img_bytes = base64.b64decode(data)
    fname = f"/tmp/{uuid.uuid4()}.{ext}"
    with open(fname, "wb") as f:
        f.write(img_bytes)
    if t == "body":
        # user can provide height in profile (not handled here) - pass None for now
        res = process_image_for_body(fname, user_height_cm=None)
        doc = {
          "user_id": user.get("_id") if user else "anon",
          "type": "body",
          "timestamp": datetime.utcnow(),
          "measurements": res.get("measurements"),
          "image_path": fname
        }
        await measurements_col.insert_one(doc)
        return res
    else:
        # face processing stub
        return {"error":"face processing not implemented in this stub"}
