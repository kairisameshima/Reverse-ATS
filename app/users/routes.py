from logging import Logger
from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.db import get_db
from app.users.domain_models import User
from app.users.repository import UserRepository
from app.users.service import UserService
import json

logger = Logger(__name__)

# Create a router for user-related endpoints
router = APIRouter()
connected_clients: List[WebSocket] = []


@router.post("/sync-users", tags=["Users"])
async def sync_users(session: Session = Depends(get_db)):
    """
    Endpoint to sync users from Slack.
    """
    user_service = UserService(session)
    result = await user_service.sync_users()
    session.flush()
    session.commit()
    user_repo = UserRepository(session)
    users = user_repo.list()
    await update_connected_clients(users)
    return {"message": result}


@router.get("/users", tags=["Users"])
def get_users(session: Session = Depends(get_db)):
    """
    Endpoint to get all users from the database.
    """
    user_repo = UserRepository(session)
    users = user_repo.list()
    return {"users": users}


@router.post("/slack-webhook", tags=["Users"])
async def slack_webhook(payload: dict, session: Session = Depends(get_db)):
    """
    Endpoint for Slack webhooks to send data to.
    """
    if payload["type"] == "url_verification":
        return {"challenge": payload["challenge"]}

    event = payload["event"]

    if event["type"] == "user_change":
        user_service = UserService(session)
        user_data_from_api = user_service.parse_slack_user(event["user"])
        user_service.add_or_update_user(user_data_from_api)
        session.flush()
        session.commit()
        users = UserRepository(session).list()
        await update_connected_clients(users)

    return {"message": "Success"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: Session = Depends(get_db)):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Wait for any message from the client (we're not using it in this example)
            await websocket.receive_text()
            # Send the current user list to the client
            users = UserRepository(session).list()
            users = [user.model_dump() for user in users]
            await websocket.send_json({"users": users})

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        logger.exception(e)
        connected_clients.remove(websocket)


async def update_connected_clients(users: List[User]):
    """
    Notify all connected clients with the updated user list.
    """
    for client in connected_clients:
        users_json = json.dumps([user.model_dump() for user in users])
        await client.send_json({"users": users_json})
