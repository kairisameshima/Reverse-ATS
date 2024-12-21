from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.applications.data_filters import ApplicationDataFilters
from app.applications.data_models import ApplicationCreateRequest
from app.applications.domain_models import Application as ApplicationModel
from app.applications.repository import ApplicationRepository
from app.db import get_db
from app.dependencies import decode_token

router = APIRouter()



@router.get("/applications")
async def get_applications(session: Session = Depends(get_db),  authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    print(decode_token(token))
    user_uuid = UUID(decode_token(token).user_id)

    application_data_filters = ApplicationDataFilters(session)
    application_uuids = application_data_filters.get_application_uuids_for_user(
        user_uuid=user_uuid
    )

    application_repository = ApplicationRepository(session)
    applications = application_repository.list(uuids=application_uuids)

    return applications
    

@router.post("/applications")
async def create_application(request: Request, session: Session = Depends(get_db), authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    user_uuid = UUID(decode_token(token).user_id)

    

    # breakpoint()

    request_data = await request.json()
    application_data = ApplicationCreateRequest(**request_data)


    application_repository = ApplicationRepository(session)
    new_application = application_repository.add(
        ApplicationModel(
            user_uuid=user_uuid,
            company_name=application_data.company,
            position=application_data.position,
            status=application_data.status,
            date_applied=application_data.dateApplied
        )
    )

    return new_application
