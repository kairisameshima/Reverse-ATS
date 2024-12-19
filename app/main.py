import os
from contextlib import asynccontextmanager

import psycopg2
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from app.db import get_db, init_db
from app.users.data_models import UserFromEndPoint
from app.users.service import UserService

load_dotenv()


app = FastAPI()
config = Config(".env")
oauth = OAuth(config)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Set up the Google OAuth provider
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    refresh_token_url=None,
    client_kwargs={"scope": "openid profile email"},
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


@asynccontextmanager  # Initialize database on startup
async def lifespan(app: FastAPI):
    init_db()
    try:
        yield
    finally:
        pass


@app.get("/db-check")
async def db_check():
    conn = psycopg2.connect(
        dbname="local_db",
        user="postgres",
        password="postgres",
        host="db",  # the service name in docker-compose.yml
        cursor_factory=RealDictCursor,
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"db_response": result}


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={
        GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=openid email profile"
    return RedirectResponse(url=google_auth_url)


@app.post("/auth/callback")
async def auth_callback(request: Request, session: Session = Depends(get_db)):
    # Verify the token
    token = request.query_params.get("token")
    id_info = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        os.getenv("GOOGLE_CLIENT_ID"),
    )

    user_from_endpoint = UserFromEndPoint(
        google_user_id=id_info["sub"],
        email=id_info["email"],
        name=id_info.get("name", "Unknown"),
        picture=id_info.get("picture", ""),
    )

    # Check if the user is already in the database
    user_service = UserService(session)
    user_uuid = user_service.get_or_create_user_from_google(
        user_from_endpoint
    )

    # Store the user's UUID in the session
    request.session["user"] = str(user_uuid)
    return RedirectResponse(url="/applications")
