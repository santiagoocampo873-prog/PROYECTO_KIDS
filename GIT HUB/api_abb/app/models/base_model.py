from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseModelWithTimestamp(BaseModel):
    """
    Modelo base que incluye timestamps.
    Sigue el principio de reutilización y abstracción.
    """
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
