from fastapi import FastAPI
from .auth import router as auth_router, get_current_user
from .routes.scans import router as scans_router
from .routes import users as users_router  # create later
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BodyMatrix API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(scans_router)
# app.include_router(users_router)
