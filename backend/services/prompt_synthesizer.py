# services/prompt_synthesizer.py
# Converts a structured DesignPlan into an optimized
# Stable Diffusion XL prompt for room visualization.

from models.design_plan import DesignPlan
from models.intake import IntakePayload


class ImagePromptSynthesizer:
    """
    Builds optimized SDXL prompts from design plans.
    The quality of the image depends heavily on prompt quality.
    """

    # Always appended to every prompt for quality
    QUALITY_TAGS = [
        "interior design photography",
        "architectural photography",
        "professional lighting",
        "8k resolution",
        "photorealistic",
        "high detail",
        "interior design magazine",
        "hyper realistic"
    ]

    # Always included in negative prompt
    NEGATIVE_PROMPT = (
        "people, humans, figures, person, cartoon, anime, "
        "illustration, painting, drawing, sketch, low quality, "
        "blurry, distorted, watermark, text, logo, "
        "dark, gloomy, horror, scary, ugly furniture, "
        "bad proportions, impossible geometry, duplicate"
    )

    def synthesize(
        self,
        plan: DesignPlan,
        intake: IntakePayload
    ) -> dict:
        """
        Build the complete image generation payload.
        Returns positive prompt, negative prompt, and parameters.
        """
        components = []

        # 1. Room foundation
        components.append(
            f"{intake.room_type.value.lower()} interior design"
        )

        # 2. Style
        components.append(
            f"{plan.recommended_theme.value.lower()} style"
        )

        # 3. LLM-extracted keywords (most valuable)
        if plan.image_prompt_keywords:
            components.extend(plan.image_prompt_keywords[:8])

        # 4. Style descriptors
        if plan.style_descriptors:
            components.extend(plan.style_descriptors[:3])

        # 5. Color palette
        if plan.color_palette:
            primary = plan.color_palette[0].name.lower()
            components.append(f"{primary} color scheme")

        # 6. Key furniture (top 2 essential items)
        essential = [
            item.name.lower()
            for item in plan.furniture_plan
            if item.priority == "essential"
        ][:2]
        components.extend(essential)

        # 7. Light level
        light_map = {
            "Bright": "bright natural light, large windows, sunlit",
            "Moderate": "soft natural light, warm ambient lighting",
            "Low": "warm artificial lighting, cozy atmosphere"
        }
        light_desc = light_map.get(
            intake.light_level.value,
            "natural lighting"
        )
        components.append(light_desc)

        # 8. Color mood
        mood_map = {
            "Warm and Cozy": "warm tones, cozy atmosphere",
            "Cool and Calm": "cool tones, serene atmosphere",
            "Bold and Vibrant": "vibrant colors, energetic",
            "Neutral and Clean": "neutral palette, clean aesthetic"
        }
        mood_desc = mood_map.get(
            intake.color_mood.value,
            "balanced atmosphere"
        )
        components.append(mood_desc)

        # 9. Quality tags
        components.extend(self.QUALITY_TAGS)

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for c in components:
            c_clean = c.strip().lower()
            if c_clean and c_clean not in seen:
                seen.add(c_clean)
                unique.append(c.strip())

        positive_prompt = ", ".join(unique)

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