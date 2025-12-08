from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AuthIn(BaseModel):
    email: str
    password: str

class ScanIn(BaseModel):
    type: str  # "body" or "face"
    image: str

class MeasurementOut(BaseModel):
    user_id: str
    type: str
    timestamp: datetime
    measurements: Optional[Dict[str, Any]]
    color_palette: Optional[list]
