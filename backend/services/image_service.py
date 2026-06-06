# services/image_service.py
# Handles image generation via HuggingFace Spaces (SDXL).
#
# RIGHT NOW: Returns a placeholder image URL for testing.
# PHASE 11: Gets replaced with real HuggingFace SDXL integration.

import asyncio
from models.design_plan import DesignPlan
from models.intake import IntakePayload


class ImageGenerationService:

    async def generate_image(
        self,
        plan: DesignPlan,
        intake: IntakePayload
    ) -> dict:
        """
        Generate a concept render from the design plan.
        Returns a job tracking dict.
        PHASE 11: Replace with real HuggingFace API call.
        """

        # Simulate the image generation delay
        await asyncio.sleep(2)

        # Return a placeholder image for now
        # This is a real interior design stock image for testing
        return {
            "job_id": f"mock-job-{plan.session_id[:8]}",
            "image_url": (
                "https://images.unsplash.com/photo-1586023492125"
                "-27b2c045efd7?w=1024&q=80"
            ),
            "status": "complete",
            "prompt_used": ", ".join(plan.image_prompt_keywords)
        }

    async def check_status(self, job_id: str) -> dict:
        """
        Check the status of an image generation job.
        PHASE 11: Replace with real HuggingFace polling.
        """
        return {
            "job_id": job_id,
            "status": "complete",
            "image_url": (
                "https://images.unsplash.com/photo-1586023492125"
                "-27b2c045efd7?w=1024&q=80"
            )
        }


# Single instance used throughout the app
image_service = ImageGenerationService()