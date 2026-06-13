# utils/helpers.py
# Helper functions used throughout the backend.

from typing import List
import re


def format_conversation_history(
    history: List[dict],
    max_turns: int = 6
) -> str:
    """
    Format conversation history for LLM prompts.
    Only keeps the most recent N turns to avoid context overflow.
    """
    if not history:
        return "No previous conversation."

    # Take only the most recent turns
    recent = history[-max_turns:]

    lines = []
    for turn in recent:
        role = "User" if turn["role"] == "user" else "Interior Designer AI"
        lines.append(f"{role}: {turn['content']}")

    return "\n".join(lines)


def format_intake_for_prompt(intake) -> str:
    """
    Convert intake form data into a readable string for LLM prompts.
    Used in refinement calls so the LLM remembers the original constraints.
    """
    must_have = (
        ", ".join(intake.must_have_items)
        if intake.must_have_items
        else "None specified"
    )

    return f"""Room Type: {intake.room_type.value}
Dimensions: {intake.get_dimensions_summary()}
Natural Light: {intake.light_level.value}
Style Preference: {intake.style_preference.value}
Color Mood: {intake.color_mood.value}
Budget Range: {intake.budget_range.value} INR
Must-Have Items: {must_have}
Items to Avoid: {intake.items_to_avoid or 'None specified'}
Special Constraints: {intake.special_constraints or 'None specified'}"""


def sanitize_session_id(session_id: str) -> bool:
    """
    Validate that a session ID looks like a real UUID.
    Prevents injection attacks.
    """
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}'
        r'-[0-9a-f]{4}-[0-9a-f]{12}$'
    )
    return bool(uuid_pattern.match(session_id.lower()))


def calculate_room_area(length: float, width: float) -> float:
    """Calculate room floor area."""
    return round(length * width, 2)