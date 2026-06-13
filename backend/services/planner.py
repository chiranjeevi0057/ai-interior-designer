# services/planner.py
# The real AI planning engine.
# Uses LangChain + Ollama (local) or Groq (production)
# to generate and refine interior design plans.

import json
from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from models.design_plan import DesignPlan
from models.intake import IntakePayload
from services.prompts import (
    SYSTEM_PROMPT,
    INITIAL_DESIGN_PROMPT,
    REFINEMENT_PROMPT
)
from services.output_parser import output_parser
from utils.helpers import format_conversation_history, format_intake_for_prompt
from config import settings


class InteriorDesignPlanner:
    """
    The AI brain of the application.
    Generates and refines interior design plans using an LLM.
    """

    def __init__(self):
        self.llm = self._initialize_llm()
        print(f"✓ AI Planner initialized with provider: {settings.llm_provider}")

    def _initialize_llm(self):
        if settings.llm_provider == "groq" and settings.groq_api_key:
            try:
                from langchain_groq import ChatGroq
                print("Using Groq API for LLM inference")
                return ChatGroq(
                    model=settings.groq_model,
                    temperature=0.3,
                    max_tokens=4000,
                    groq_api_key=settings.groq_api_key
                )
            except Exception as e:
                print(f"Groq initialization failed: {e}. Falling back to Ollama.")

        print(f"Using local Ollama with model: {settings.ollama_model}")
        return ChatOllama(
            model=settings.ollama_model,
            temperature=0.1,
            format="json",
            num_predict=3000,
            num_ctx=4096,
            base_url="http://127.0.0.1:11434"
        )

    async def generate_plan(
        self,
        intake: IntakePayload,
        session_id: str
    ) -> DesignPlan:
        """
        Generate a complete design plan from intake form data.
        Makes a real LLM call and validates the response.
        """
        print(f"\n{'='*50}")
        print(f"Generating design plan for session: {session_id}")
        print(f"Room: {intake.room_type}, {intake.get_dimensions_summary()}")
        print(f"Style: {intake.style_preference}, Budget: {intake.budget_range}")
        print(f"{'='*50}")

        # Build the prompt
        user_prompt = self._build_initial_prompt(intake, session_id)

        # Make the LLM call with retry logic
        result = await self._call_llm_with_retry(
            user_prompt=user_prompt,
            session_id=session_id,
            max_retries=2
        )

        if result is None:
            print("LLM failed to return valid JSON. Using fallback plan.")
            return self._create_fallback_plan(intake, session_id)

        print(f"✓ Design plan generated successfully (version {result.version})")
        return result

    async def refine_plan(
        self,
        session,
        user_message: str
    ) -> DesignPlan:
        """
        Refine an existing design plan based on user feedback.
        Sends full context to the LLM so it understands the history.
        """
        current_plan = session.current_plan
        print(f"\n{'='*50}")
        print(f"Refining plan for session: {session.session_id}")
        print(f"User request: {user_message}")
        print(f"Current version: {current_plan.version}")
        print(f"{'='*50}")

        # Format conversation history
        history = format_conversation_history(
            session.conversation_history,
            max_turns=6
        )

        # Format the original intake
        original_intake = format_intake_for_prompt(session.intake)

        # Build the refinement prompt
        user_prompt = REFINEMENT_PROMPT.format(
            original_intake=original_intake,
            current_version=current_plan.version,
            current_plan=current_plan.model_dump_json(indent=2),
            conversation_history=history,
            user_message=user_message,
            next_version=current_plan.version + 1
        )

        # Make the LLM call
        result = await self._call_llm_with_retry(
            user_prompt=user_prompt,
            session_id=session.session_id,
            max_retries=2
        )

        if result is None:
            print("Refinement failed. Returning current plan with warning.")
            # Return current plan with a warning rather than crashing
            return current_plan.model_copy(
                update={
                    "version": current_plan.version + 1,
                    "design_warnings": [
                        f"Could not process request: '{user_message}'. "
                        "Please try rephrasing your request."
                    ],
                    "requires_visual_update": False,
                }
            )

        print(f"✓ Plan refined successfully (version {result.version})")
        return result

    async def _call_llm_with_retry(
        self,
        user_prompt: str,
        session_id: str,
        max_retries: int = 2
    ) -> Optional[DesignPlan]:
        """
        Call the LLM and retry if the output is invalid.
        This handles the common case where the LLM returns
        slightly malformed JSON on the first attempt.
        """
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]

        for attempt in range(max_retries):
            try:
                print(f"LLM call attempt {attempt + 1}/{max_retries}...")

                # Make the actual LLM call
                response = await self.llm.ainvoke(messages)
                raw_output = response.content

                print(f"Raw output length: {len(raw_output)} characters")
                print(f"First 200 chars: {raw_output[:200]}")

                # Try to parse the output
                plan = output_parser.parse(raw_output, session_id)

                if plan is not None:
                    return plan

                # If parsing failed, add correction instruction
                print(f"Attempt {attempt + 1} failed — output was not valid JSON")

                if attempt < max_retries - 1:
                    # Add a correction message for the next attempt
                    messages.append(HumanMessage(
                        content=f"Your previous response was not valid JSON. "
                                f"You returned: {raw_output[:500]}... "
                                f"Please return ONLY valid JSON matching the schema. "
                                f"No markdown, no backticks, no explanation text."
                    ))

            except Exception as e:
                print(f"LLM call error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise

        return None

    def _build_initial_prompt(
        self,
        intake: IntakePayload,
        session_id: str
    ) -> str:
        """Build the initial design generation prompt from intake data."""

        must_have = (
            ", ".join(intake.must_have_items)
            if intake.must_have_items
            else "None specified"
        )

        return INITIAL_DESIGN_PROMPT.format(
            room_type=intake.room_type.value,
            dimensions_summary=intake.get_dimensions_summary(),
            area=intake.get_area(),
            unit="ft" if intake.unit.value == "feet" else "m",
            light_level=intake.light_level.value,
            style_preference=intake.style_preference.value,
            color_mood=intake.color_mood.value,
            budget_range=intake.budget_range.value,
            must_have_items=must_have,
            items_to_avoid=intake.items_to_avoid or "None",
            special_constraints=intake.special_constraints or "None",
            session_id=session_id
        )

    def _create_fallback_plan(
        self,
        intake: IntakePayload,
        session_id: str
    ) -> DesignPlan:
        """
        Returns a basic but valid plan when the LLM completely fails.
        This ensures the app never crashes due to LLM issues.
        """
        from models.design_plan import (
            RoomTheme, ColorSwatch, FurnitureItem, LightingItem
        )

        # Map style preference to theme
        theme_map = {
            "Minimalist": RoomTheme.MINIMALIST,
            "Scandinavian": RoomTheme.SCANDINAVIAN,
            "Industrial": RoomTheme.INDUSTRIAL,
            "Bohemian": RoomTheme.BOHEMIAN,
            "Contemporary": RoomTheme.CONTEMPORARY,
            "Traditional": RoomTheme.TRADITIONAL,
            "Mid-Century Modern": RoomTheme.MID_CENTURY_MODERN,
            "Japandi": RoomTheme.JAPANDI,
        }
        theme = theme_map.get(
            intake.style_preference.value,
            RoomTheme.CONTEMPORARY
        )

        return DesignPlan(
            session_id=session_id,
            version=1,
            room_type=intake.room_type.value,
            room_dimensions_summary=intake.get_dimensions_summary(),
            spatial_observations=[
                f"Room area of {intake.get_area()} sq ft analyzed.",
                f"{intake.light_level.value} natural light noted.",
            ],
            recommended_theme=theme,
            theme_rationale=(
                f"The {intake.style_preference.value} theme was selected "
                f"based on your preferences."
            ),
            color_palette=[
                ColorSwatch(name="Warm White", hex_code="#F5F5F0",
                           usage="Primary wall color"),
                ColorSwatch(name="Natural Oak", hex_code="#C4A265",
                           usage="Wood furniture tones"),
                ColorSwatch(name="Charcoal", hex_code="#4A4A4A",
                           usage="Accent pieces"),
                ColorSwatch(name="Soft Taupe", hex_code="#B8A99A",
                           usage="Secondary surfaces"),
            ],
            color_palette_notes="A balanced neutral palette suitable for the chosen style.",
            furniture_plan=[
                FurnitureItem(
                    id="item_1",
                    name="Primary Seating",
                    category="Seating",
                    recommended_dimensions="200cm W x 85cm D x 80cm H",
                    placement="Against the main wall, centered",
                    placement_reasoning="Anchors the room and maximizes open space.",
                    priority="essential",
                    estimated_cost_range="15000-40000"
                ),
            ],
            furniture_plan_notes="Layout optimized for the available space.",
            traffic_flow_notes="90cm clearance maintained on primary pathways.",
            lighting_plan=[
                LightingItem(
                    type="Ambient",
                    description="Ceiling LED panel",
                    placement="Center of ceiling",
                    reasoning="Provides even base illumination."
                ),
            ],
            key_design_principles=[
                "Focal point established",
                "Traffic flow maintained",
                "Scale appropriate to room dimensions",
            ],
            design_warnings=["AI response was incomplete. Please try regenerating."],
            budget_tier=intake.budget_range.value,
            estimated_total_range="30000-80000",
            budget_notes="Prioritize essential pieces first.",
            image_prompt_keywords=[
                intake.room_type.value.lower(),
                intake.style_preference.value.lower(),
                "interior design", "natural light", "professional photography"
            ],
            style_descriptors=["clean", "functional", "balanced"],
            requires_visual_update=False,
        )


# Single instance used throughout the app
planner = InteriorDesignPlanner()