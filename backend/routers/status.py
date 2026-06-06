# routers/status.py
# Endpoints for checking image generation status.
# The frontend calls these every 5 seconds while waiting
# for the concept render to be ready.

from fastapi import APIRouter, HTTPException
from models.responses import ImageStatusResponse, SessionStatusResponse
from session.store import session_store
from utils.helpers import sanitize_session_id

router = APIRouter(prefix="/api/status", tags=["Status"])


@router.get("/image/{session_id}", response_model=ImageStatusResponse)
async def get_image_status(session_id: str):
    """
    Check if the concept render image is ready.
    Frontend polls this every 5 seconds.

    Returns:
    - pending:    Image generation not started yet
    - generating: Image is being created on HuggingFace
    - complete:   Image is ready — image_url is included
    - failed:     Image generation failed — plan still available
    """

    if not sanitize_session_id(session_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID."
        )

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or expired."
        )

    return ImageStatusResponse(
        success=True,
        session_id=session_id,
        image_status=session.image_status,
        image_url=session.image_url if session.image_status == "complete"
                  else None,
        message=_get_status_message(session.image_status)
    )


@router.get("/session/{session_id}", response_model=SessionStatusResponse)
async def get_session_status(session_id: str):
    """
    Get the full status of a design session.
    """

    if not sanitize_session_id(session_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID."
        )

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or expired."
        )

    return SessionStatusResponse(
        success=True,
        session_id=session_id,
        session_state=session.session_state,
        image_status=session.image_status,
        plan_version=session.current_plan.version
                     if session.current_plan else 0,
        image_url=session.image_url
    )


def _get_status_message(status: str) -> str:
    """Human-readable message for each image status."""
    messages = {
        "pending":    "Image generation is queued.",
        "generating": "Your concept render is being created...",
        "complete":   "Your concept render is ready!",
        "failed":     "Image generation failed. Your design plan is still available.",
    }
    return messages.get(status, "Unknown status.")