from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ScheduleJob(BaseModel):
    job_id: str
    post_id: int
    variant_id: int
    scheduled_at: datetime


class ScheduleJobResponse(BaseModel):
    status: str
    job_id: str


class ScheduleJobsList(BaseModel):
    jobs: List[ScheduleJob]


class ScheduleJobCancel(BaseModel):
    status: str