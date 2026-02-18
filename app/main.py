"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.role import Role, UserRole
from app.models.organization import Organization
from app.models.election import Election, Candidate, Voter
from app.models.vote import Vote

from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.api.organization_routes import router as org_router
from app.api.election_routes import router as election_router
from app.api.vote_routes import router as vote_router

settings = get_settings()

# System roles
SYSTEM_ROLES = ["SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER", "VOTER"]


def seed_database():
    """Seed roles and super admin on startup."""
    db = SessionLocal()
    try:
        # Seed roles
        for role_name in SYSTEM_ROLES:
            existing = db.query(Role).filter(Role.name == role_name).first()
            if not existing:
                db.add(Role(name=role_name))
        db.commit()

        # Seed super admin
        admin = db.query(User).filter(User.email == settings.SUPER_ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=settings.SUPER_ADMIN_EMAIL,
                password_hash=hash_password(settings.SUPER_ADMIN_PASSWORD),
                full_name="Super Admin",
                is_active=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

            # Assign SUPER_ADMIN role
            super_admin_role = db.query(Role).filter(Role.name == "SUPER_ADMIN").first()
            if super_admin_role:
                db.add(UserRole(user_id=admin.id, role_id=super_admin_role.id))
                db.commit()

            print(f"✅ Super admin created: {settings.SUPER_ADMIN_EMAIL}")
        else:
            print(f"ℹ️  Super admin already exists: {settings.SUPER_ADMIN_EMAIL}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — create tables and seed data on startup."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    # Seed roles and super admin
    seed_database()

    yield

    print("🛑 Application shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="A secure, role-based online voting platform for private organizations.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Include API routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(org_router)
app.include_router(election_router)
app.include_router(vote_router)


@app.get("/")
def root():
    """Redirect to login page."""
    return RedirectResponse(url="/static/login.html")


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
