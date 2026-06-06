# models/responses.py
# These are the exact shapes of data the API sends back
# to the frontend. Every endpoint returns one of these.

from pydantic import BaseModel
from typing import Optional, Any
from models.design_plan import DesignPlan


class APIResponse(BaseModel):
    """Base response wrapper for all API responses."""
    success: bool
    message: str
    data: Optional[Any] = None


class DesignGenerateResponse(BaseModel):
    """Response when a new design plan is generated."""
    success: bool
    session_id: str
    session_state: str
    design_plan: DesignPlan
    image_status: str  # "generating" — image is being made in background
    message: str


class DesignRefineResponse(BaseModel):
    """Response when a design is refined/updated."""
    success: bool
    session_id: str
    session_state: str
    design_plan: DesignPlan
    image_status: str
    requires_visual_update: bool
    message: str


class ImageStatusResponse(BaseModel):
    """Response when frontend polls for image status."""
    success: bool
    session_id: str
    image_status: str       # pending, generating, complete, failed
    image_url: Optional[str] = None
    message: str


class SessionStatusResponse(BaseModel):
    """Response with full session status."""
    success: bool
    session_id: str
    session_state: str
    image_status: str
    plan_version: int
    image_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Response when something goes wrong."""
    success: bool = False
    error_code: str
    message: str
    detail: Optional[str] = None