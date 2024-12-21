from datetime import datetime
from typing import Optional
from uuid import UUID

from app.db import ApplicationStageStatus, ApplicationStatus
from app.lib.data_access.domain_model import DomainModel


class ApplicationStage(DomainModel):
    """ApplicationStage domain model."""
    application_uuid: UUID
    name: str
    status: ApplicationStageStatus = ApplicationStageStatus.PENDING
    date_scheduled: Optional[datetime]
    date_occurred: Optional[datetime]
    notes: Optional[str]


class Application(DomainModel):
    """Application domain model."""
    company_name: str
    description: Optional[str] = None
    user_uuid: UUID
    position: str
    status: ApplicationStatus = ApplicationStatus.PROSPECT
    date_applied: Optional[datetime] = None
    date_first_response: Optional[datetime] = None
    date_rejected: Optional[datetime] = None


class MutableApplicationFields:
    """Fields that can be updated on a Application."""
    company_name: str
    description: str
    position: str
    status: ApplicationStatus
    date_applied: datetime
    date_first_response: datetime
    date_rejected: datetime
