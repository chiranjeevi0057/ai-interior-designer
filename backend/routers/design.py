# routers/design.py
# All API endpoints related to design generation and refinement.
#
# POST /api/design/generate  → Generate a new design plan
# POST /api/design/refine    → Refine an existing design plan
# GET  /api/design/{id}      → Get current design plan

import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.intake import IntakePayload
from models.responses import (
    DesignGenerateResponse,
    DesignRefineResponse,
    ErrorResponse
)
from session.store import session_store
from services.planner import planner
from services.image_service import image_service
from utils.helpers import sanitize_session_id

# Create the router — all routes here get the /api/design prefix
router = APIRouter(prefix="/api/design", tags=["Design"])


async def run_image_generation(session_id: str):
    """
    Background task: generates image after plan is ready.
    Runs separately so the user gets the plan immediately
    without waiting for the image.
    """
    session = session_store.get(session_id)
    if not session or not session.current_plan:
        return

    try:
        # Update status so frontend knows image is being made
        session.image_status = "generating"
        session.session_state = "image_generating"

        # Call the image generation service
        result = await image_service.generate_image(
            plan=session.current_plan,
            intake=session.intake
        )

        # Store the result in the session
        session.image_url = result["image_url"]
        session.image_job_id = result["job_id"]
        session.image_status = "complete"
        session.session_state = "complete"
        session.image_prompt = result["prompt_used"]

    except Exception as e:
        # Image generation failed — plan is still available
        session.image_status = "failed"
        session.session_state = "plan_ready"
        print(f"Image generation failed for session {session_id}: {e}")


@router.post("/generate", response_model=DesignGenerateResponse)
async def generate_design(
    intake: IntakePayload,
    background_tasks: BackgroundTasks
):
    """
    Generate a new interior design plan.

    1. Validates the intake form data (automatic via Pydantic)
    2. Creates a new session
    3. Calls the AI planner to generate a design plan
    4. Starts image generation in the background
    5. Returns the design plan immediately (no waiting for image)
    """

    # Create a new session to track this design request
    session = session_store.create(intake)
    session.session_state = "planning"

    try:
        # Generate the design plan (this is the AI call)
        # Currently returns mock data — real AI in Phase 9
        design_plan = await planner.generate_plan(
            intake=intake,
            session_id=session.session_id
        )

        # Store the plan in the session
        session.current_plan = design_plan
        session.session_state = "plan_ready"

        # Add the AI's plan to conversation history
        session.add_conversation_turn(
            role="assistant",
            content=f"Generated design plan version {design_plan.version}"
        )

        # Start image generation in background
        # This runs AFTER we return the response to the frontend
        background_tasks.add_task(
            run_image_generation,
            session.session_id
        )

        return DesignGenerateResponse(
            success=True,
            session_id=session.session_id,
            session_state=session.session_state,
            design_plan=design_plan,
            image_status="generating",
            message="Design plan generated successfully. "
                    "Concept render is being prepared."
        )

    except Exception as e:
        # If planning fails, mark session as failed
        session.session_state = "failed"
        raise HTTPException(
            status_code=500,
            detail=f"Design generation failed: {str(e)}"
        )


@router.post("/refine", response_model=DesignRefineResponse)
async def refine_design(
    session_id: str,
    user_message: str,
    background_tasks: BackgroundTasks
):
    """
    Refine an existing design plan based on user feedback.

    1. Validates the session exists and is active
    2. Adds user message to conversation history
    3. Calls AI planner with full context to update the plan
    4. If visual update needed, starts new image generation
    5. Returns the updated design plan
    """

    # Validate session ID format
    if not sanitize_session_id(session_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID format."
        )

    # Get the session
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or expired. "
                   "Please start a new design."
        )

    if not session.current_plan:
        raise HTTPException(
            status_code=400,
            detail="No design plan found in this session."
        )

    # Add user message to conversation history
    session.add_conversation_turn(
        role="user",
        content=user_message
    )

    try:
        # Refine the plan based on user message
        session.session_state = "planning"
        updated_plan = await planner.refine_plan(
            session=session,
            user_message=user_message
        )

        # Update the session
        session.current_plan = updated_plan
        session.session_state = "plan_ready"

        # Add AI response to conversation history
        session.add_conversation_turn(
            role="assistant",
            content=f"Updated design plan to version {updated_plan.version}"
        )

        # Only regenerate image if the plan significantly changed
        if updated_plan.requires_visual_update:
            session.image_status = "pending"
            background_tasks.add_task(
                run_image_generation,
                session.session_id
            )

        return DesignRefineResponse(
            success=True,
            session_id=session.session_id,
            session_state=session.session_state,
            design_plan=updated_plan,
            image_status=session.image_status,
            requires_visual_update=updated_plan.requires_visual_update,
            message="Design plan updated successfully."
        )

    except Exception as e:
        session.session_state = "plan_ready"
        raise HTTPException(
            status_code=500,
            detail=f"Refinement failed: {str(e)}"
        )


@router.get("/{session_id}")
async def get_design(session_id: str):
    """
    Get the current design plan for a session.
    Used when the frontend needs to reload the current state.
    """

    if not sanitize_session_id(session_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID format."
        )

    session = session_store.get(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or expired."
        )

    return {
        "success": True,
        "session_id": session.session_id,
        "session_state": session.session_state,
        "design_plan": session.current_plan,
        "image_status": session.image_status,
        "image_url": session.image_url,
    }