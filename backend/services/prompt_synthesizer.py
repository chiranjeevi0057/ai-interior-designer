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
        room = intake.room_type.value
        style = plan.recommended_theme.value
        light = intake.light_level.value

        primary_color = (
            plan.color_palette[0].name
            if plan.color_palette else "neutral white"
        )
        secondary_color = (
            plan.color_palette[1].name
            if len(plan.color_palette) > 1 else "warm beige"
        )

        # Room-specific scene descriptions
        # These explicitly describe what should be IN the image
        room_scene_map = {
            "Living Room": (
            "featuring a sofa, coffee table, and TV unit. "
            "Comfortable seating area with decorative cushions"
        ),
        "Bedroom": (
            "featuring a large bed with headboard, wardrobe, "
            "and bedside tables. Relaxing sleeping environment"
        ),
        "Home Office": (
            "featuring a large work desk, ergonomic office chair, "
            "and bookshelves. Professional productive workspace"
        ),
        "Dining Room": (
            "featuring a dining table with chairs and a sideboard. "
            "Elegant space for family meals"
        ),
        "Studio Apartment": (
            "featuring multifunctional furniture including a sofa bed "
            "and compact dining area. Smart small space design"
        ),
        }
        room_scene = room_scene_map.get(
            room,
            "featuring appropriate furniture for the space"
        )

        # Light descriptions
        light_map = {
        "Bright": "flooded with bright natural sunlight through large windows",
        "Moderate": "softly lit with warm natural light",
        "Low": "warmly lit with layered artificial lighting"
        }
        light_desc = light_map.get(light, "naturally lit")

        # Style-specific visual details
        style_map = {
        "Scandinavian": "light birch wood, white walls, linen textiles, hygge atmosphere",
        "Minimalist": "clean lines, white space, essential furniture only, zen calm",
        "Industrial": "exposed concrete, metal accents, Edison bulbs, raw urban aesthetic",
        "Bohemian": "layered rugs, plants, eclectic cushions, warm earthy tones",
        "Contemporary": "sleek surfaces, neutral palette, clean geometry, modern finishes",
        "Traditional": "rich wood tones, classic moldings, elegant fabrics, timeless style",
        "Mid-Century Modern": "tapered legs, organic curves, retro palette, teak wood",
        "Japandi": "natural wood, wabi-sabi, muted tones, minimal decor, bamboo accents"
        }
        style_desc = style_map.get(style, "tastefully decorated")

        # Build the prompt — room type appears 3 times for emphasis
        positive_prompt = (
        f"A beautifully designed {style} {room.lower()}, "
        f"{room_scene}. "
        f"The {room.lower()} is {light_desc}. "
        f"Color palette features {primary_color} and {secondary_color}. "
        f"Interior design style: {style_desc}. "
        f"This is a {room.lower()} — photographed as a professional "
        f"interior design shoot, ultra photorealistic, 8k, "
        f"architectural digest quality, perfect lighting, no people."
        )
        
        return {
        "positive_prompt": positive_prompt,
        "negative_prompt": self.NEGATIVE_PROMPT,
        "width": 1280,
        "height": 960,
        "num_inference_steps": 25,
        "guidance_scale": 7.5,
        }


# Single instance
prompt_synthesizer = ImagePromptSynthesizer()