# services/prompt_synthesizer.py
# Builds optimized prompts for Flux model via Pollinations AI.
# Flux works better with natural language descriptions
# than keyword-heavy SDXL prompts.

from models.design_plan import DesignPlan
from models.intake import IntakePayload


class ImagePromptSynthesizer:

    NEGATIVE_PROMPT = (
        "people, humans, figures, person, cartoon, anime, "
        "illustration, painting, drawing, sketch, low quality, "
        "blurry, distorted, watermark, text, logo, "
        "dark, gloomy, horror, ugly furniture, bad proportions"
    )

    def synthesize(
        self,
        plan: DesignPlan,
        intake: IntakePayload
    ) -> dict:
        """
        Build a natural language prompt optimized for Flux model.
        More descriptive and specific than keyword lists.
        """

        # Room and style foundation
        room = intake.room_type.value
        style = plan.recommended_theme.value
        light = intake.light_level.value

        # Get primary color
        primary_color = (
            plan.color_palette[0].name
            if plan.color_palette else "neutral"
        )
        secondary_color = (
            plan.color_palette[1].name
            if len(plan.color_palette) > 1 else "warm white"
        )

        # Get essential furniture pieces
        essential_furniture = [
            item.name for item in plan.furniture_plan
            if item.priority == "essential"
        ][:3]

        furniture_str = (
            ", ".join(essential_furniture)
            if essential_furniture
            else "appropriate furniture"
        )

        # Light description
        light_map = {
            "Bright": "flooded with bright natural sunlight through large windows",
            "Moderate": "softly lit with warm natural light",
            "Low": "warmly lit with soft artificial lighting and cozy atmosphere"
        }
        light_desc = light_map.get(light, "naturally lit")

        # Color mood description
        mood_map = {
            "Warm and Cozy": "warm and inviting with cozy atmosphere",
            "Cool and Calm": "cool and serene with calm atmosphere",
            "Bold and Vibrant": "bold and energetic with vibrant colors",
            "Neutral and Clean": "clean and minimal with neutral tones"
        }
        mood_desc = mood_map.get(
            intake.color_mood.value,
            "balanced and harmonious"
        )

        # Style specific additions
        style_additions = {
            "Scandinavian": "light wood accents, white walls, clean lines, hygge atmosphere",
            "Minimalist": "clean lines, uncluttered space, essential furniture only, zen atmosphere",
            "Industrial": "exposed brick or concrete, metal accents, raw materials, urban feel",
            "Bohemian": "layered textiles, plants, eclectic decor, warm colors, artistic",
            "Contemporary": "sleek modern furniture, neutral palette, glass and metal accents",
            "Traditional": "classic furniture, rich wood tones, elegant decor, timeless style",
            "Mid-Century Modern": "organic shapes, tapered legs, retro palette, vintage feel",
            "Japandi": "wabi-sabi aesthetic, natural materials, muted tones, zen simplicity"
        }
        style_desc = style_additions.get(style, "tastefully decorated")

        # Build natural language prompt
        positive_prompt = (
            f"A beautifully designed {style} {room.lower()}, "
            f"{light_desc}. "
            f"The room features {furniture_str}. "
            f"Color scheme uses {primary_color} and {secondary_color} tones. "
            f"The space is {mood_desc}. "
            f"Interior design details include {style_desc}. "
            f"Shot as professional interior design photography, "
            f"ultra realistic, 8k resolution, perfect composition, "
            f"architectural digest quality, no people."
        )

        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": self.NEGATIVE_PROMPT,
            "width": 1024,
            "height": 768,
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
        }


# Single instance
prompt_synthesizer = ImagePromptSynthesizer()