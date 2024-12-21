from datetime import date
from typing import Optional
from uuid import UUID

from app.db import ApplicationStageStatus, ApplicationStatus
from app.lib.data_access.domain_model import DomainModel


class ApplicationStage(DomainModel):
    """ApplicationStage domain model."""
    application_uuid: UUID
    name: str
    status: ApplicationStageStatus = ApplicationStageStatus.PENDING
    date_scheduled: Optional[date]
    date_occurred: Optional[date]
    notes: Optional[str]


class Application(DomainModel):
    """Application domain model."""
    company: str
    description: Optional[str] = None
    user_uuid: UUID
    position: str
    status: ApplicationStatus = ApplicationStatus.PROSPECT
    date_applied: Optional[date] = None
    date_first_response: Optional[date] = None
    date_rejected: Optional[date] = None


class MutableApplicationFields:
    """Fields that can be updated on a Application."""
    company: str
    description: str
    position: str
    status: ApplicationStatus
    date_applied: date
    date_first_response: date
    date_rejected: date
