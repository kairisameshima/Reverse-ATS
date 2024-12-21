from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApplicationCreateRequest(BaseModel):
    company: str
    position: str
    status: str
    dateApplied: Optional[datetime] = None

