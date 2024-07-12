"""API routes for the app."""

from fastapi import APIRouter

from app.api.routes import retrieval_route

api_router = APIRouter()

api_router.include_router(retrieval_route.router)
