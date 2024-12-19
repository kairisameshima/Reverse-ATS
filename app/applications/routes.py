from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.applications.data_filters import ApplicationDataFilters
from app.applications.repository import ApplicationRepository
from app.db import get_db

router = APIRouter()


async def get_user_uuid(request: Request):
    return request.session.get("user_uuid")


# @router.get("/applications")
# async def get_applications(request: Request, session: Session = Depends(get_db)):
#     user_uuid = request.session.get("user_uuid")
#     breakpoint()
#     application_data_filters = ApplicationDataFilters(session)
#     application_uuids = application_data_filters.get_application_uuids_for_user(
#         user_uuid=user_uuid
#     )

#     application_repository = ApplicationRepository(session)
#     applications = application_repository.list(uuids=application_uuids)

#     return applications


@router.post("/applications")
async def create_application():
    user_uuid = Depends(get_user_uuid)

    # breakpoint()

    # request_data = await Request.json()
    # application_data = ApplicationCreateRequest(**request_data)

    # if not application_data.name or not application_data.description:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Name and description are required fields"
    #     )

    # application_repository = ApplicationRepository(session)
    # new_application = application_repository.create(
    #     user_uuid=user_uuid,
    #     name=application_data.name,
    #     description=application_data.description
    # )

    # return new_application
    return []
