# services/planner.py
# AI Planning Service — connects to Ollama/Groq via LangChain.
#
# RIGHT NOW: Returns a hardcoded mock design plan so we can
# test all the API endpoints without needing Ollama running.
#
# PHASE 9: This gets replaced with real LangChain + Ollama logic.

from models.design_plan import (
    DesignPlan, RoomTheme, ColorSwatch,
    FurnitureItem, LightingItem
)
from models.intake import IntakePayload


class InteriorDesignPlanner:

    async def generate_plan(
        self,
        intake: IntakePayload,
        session_id: str
    ) -> DesignPlan:
        """
        Generate a complete design plan from intake form data.
        PHASE 9: Replace mock with real LangChain + LLM call.
        """

        # ── MOCK RESPONSE (temporary until Phase 9) ──────────────
        # This returns a realistic-looking plan so the entire
        # frontend and backend can be built and tested now.
        return DesignPlan(
            session_id=session_id,
            version=1,
            room_type=intake.room_type.value,
            room_dimensions_summary=intake.get_dimensions_summary(),
            spatial_observations=[
                f"The {intake.get_area()} sq ft floor area suits "
                f"a {intake.style_preference.value} layout well.",
                f"{intake.light_level.value} natural light influences "
                f"the color palette selection.",
                "Standard ceiling height allows full furniture range."
            ],
            recommended_theme=RoomTheme(intake.style_preference.value)
            if intake.style_preference.value in [t.value for t in RoomTheme]
            else RoomTheme.CONTEMPORARY,
            theme_rationale=(
                f"The {intake.style_preference.value} theme suits your "
                f"{intake.room_type.value} given the available space and "
                f"{intake.light_level.value.lower()} natural light conditions."
            ),
            color_palette=[
                ColorSwatch(
                    name="Warm White",
                    hex_code="#F5F5F0",
                    usage="Primary wall color"
                ),
                ColorSwatch(
                    name="Soft Taupe",
                    hex_code="#B8A99A",
                    usage="Secondary accent walls"
                ),
                ColorSwatch(
                    name="Natural Oak",
                    hex_code="#C4A265",
                    usage="Wood furniture tones"
                ),
                ColorSwatch(
                    name="Charcoal",
                    hex_code="#4A4A4A",
                    usage="Accent pieces and frames"
                ),
            ],
            color_palette_notes=(
                "This palette creates a calm, cohesive feel that "
                "complements the chosen style."
            ),
            furniture_plan=[
                FurnitureItem(
                    id="item_1",
                    name="3-Seater Sofa",
                    category="Seating",
                    recommended_dimensions="220cm W x 90cm D x 85cm H",
                    placement="Against the main wall, centered",
                    placement_reasoning=(
                        "Anchors the seating area and maximizes "
                        "open floor space for traffic flow."
                    ),
                    priority="essential",
                    estimated_cost_range="15000-45000"
                ),
                FurnitureItem(
                    id="item_2",
                    name="Coffee Table",
                    category="Tables",
                    recommended_dimensions="120cm W x 60cm D x 45cm H",
                    placement="Centered in front of sofa, 45cm gap",
                    placement_reasoning=(
                        "Standard 45cm gap allows comfortable leg room "
                        "while keeping items within easy reach."
                    ),
                    priority="essential",
                    estimated_cost_range="5000-15000"
                ),
                FurnitureItem(
                    id="item_3",
                    name="TV Unit",
                    category="Storage",
                    recommended_dimensions="150cm W x 40cm D x 50cm H",
                    placement="On the wall opposite the sofa",
                    placement_reasoning=(
                        "Creates the room focal point and maintains "
                        "comfortable viewing distance."
                    ),
                    priority="essential",
                    estimated_cost_range="8000-20000"
                ),
            ],
            furniture_plan_notes=(
                "Furniture is arranged to maximize open floor space "
                "while creating a clear focal point."
            ),
            traffic_flow_notes=(
                "A minimum 90cm walkway is maintained on all primary "
                "paths through the room."
            ),
            lighting_plan=[
                LightingItem(
                    type="Ambient",
                    description="Ceiling-mounted LED panel light",
                    placement="Center of ceiling",
                    reasoning="Provides even base illumination across the room."
                ),
                LightingItem(
                    type="Accent",
                    description="Floor lamp with warm bulb",
                    placement="Corner beside the sofa",
                    reasoning=(
                        "Creates a warm reading corner and adds "
                        "depth to the room at night."
                    )
                ),
            ],
            key_design_principles=[
                "Focal point established with TV wall as the visual anchor",
                "60-30-10 color rule applied across walls, furniture, and accents",
                "Traffic flow maintained with 90cm minimum clearance",
            ],
            design_warnings=[],
            budget_tier=intake.budget_range.value,
            estimated_total_range="35000-80000",
            budget_notes=(
                "Prioritise sofa and lighting first. "
                "Coffee table and storage can be added gradually."
            ),
            image_prompt_keywords=[
                intake.room_type.value.lower(),
                intake.style_preference.value.lower(),
                "interior design",
                "natural light",
                "warm tones",
                "professional photography",
            ],
            style_descriptors=[
                "clean and airy",
                "warm neutral tones",
                "functional layout",
            ],
            requires_visual_update=False,
        )

    async def refine_plan(
        self,
        session,
        user_message: str
    ) -> DesignPlan:
        """
        Refine existing plan based on user message.
        PHASE 9: Replace with real LangChain refinement chain.
        """
        current_plan = session.current_plan

        # For now just increment version and note the change
        updated_plan = current_plan.model_copy(
            update={
                "version": current_plan.version + 1,
                "design_warnings": [
                    f"Refinement requested: '{user_message}' "
                    f"(AI integration coming in Phase 9)"
                ],
                "requires_visual_update": False,
            }
        )
        return updated_plan


# Single instance used throughout the app
planner = InteriorDesignPlanner()