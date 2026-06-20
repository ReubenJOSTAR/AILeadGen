from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeadBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    budget_range: Optional[str] = None
    campaign_type: Optional[str] = None
    timeline: Optional[str] = None
    call_time_pref: Optional[str] = None
    requirements: Optional[str] = None


class LeadCreate(LeadBase):
    widget_id: str
    session_id: str


class Lead(LeadBase):
    id: str
    widget_id: str
    session_id: str
    status: str = "new"
    raw_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class LeadUpdate(BaseModel):
    status: Optional[str] = None
