# services/image_service.py
# Generates concept renders using multiple free services.
# Tries each method in order until one works.

import asyncio
import httpx
from urllib.parse import quote
from models.design_plan import DesignPlan
from models.intake import IntakePayload
from services.prompt_synthesizer import prompt_synthesizer


class ImageGenerationService:
    """
    Generates room concept renders using free image generation APIs.
    Falls back gracefully through multiple providers.
    """

    def __init__(self):
        print("✓ Image Service initialized")

    async def generate_image(
        self,
        plan: DesignPlan,
        intake: IntakePayload
    ) -> dict:
        """
        Generate a concept render from the design plan.
        Tries multiple methods in order.
        """
        # Build the optimized prompt
        prompt_data = prompt_synthesizer.synthesize(plan, intake)
        prompt = prompt_data["positive_prompt"]
        negative = prompt_data["negative_prompt"]

        print(f"\n Generating image for session: {plan.session_id}")
        print(f"Prompt preview: {prompt[:120]}...")

        # Method 1 — Pollinations AI (free, no key needed)
        result = await self._generate_via_pollinations(prompt)
        if result:
            return result

        # Method 2 — Stable Horde (free community GPU)
        result = await self._generate_via_stable_horde(prompt, negative)
        if result:
            return result

        # Method 3 — Fallback curated photo
        print("All methods failed — using fallback photo")
        return self._get_fallback_image(intake.room_type.value)

    async def _generate_via_pollinations(
        self,
        prompt: str
    ) -> dict | None:
        """
        Generate using Pollinations.ai — completely free, no API key.
        Returns image as a URL directly.
        """
        try:
            print("Trying Pollinations AI...")

            # Pollinations generates images via URL
            # We just need to encode the prompt and request the image
            encoded_prompt = quote(prompt)
            image_url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                f"?width=1024&height=768&model=flux&nologo=true&enhance=true"
            )

            # Verify the URL is reachable
            async with httpx.AsyncClient(timeout=90) as client:
                response = await client.get(
                    image_url,
                    follow_redirects=True
                )

                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    if "image" in content_type:
                        print("✓ Image generated via Pollinations AI")
                        return {
                            "job_id": "pollinations",
                            "image_url": image_url,
                            "status": "complete",
                            "prompt_used": prompt,
                            "method": "pollinations"
                        }
                    else:
                        print(f"Pollinations returned non-image: {content_type}")
                        return None
                else:
                    print(f"Pollinations status: {response.status_code}")
                    return None

        except Exception as e:
            print(f"Pollinations failed: {e}")
            return None

    async def _generate_via_stable_horde(
        self,
        prompt: str,
        negative_prompt: str
    ) -> dict | None:
        """
        Generate using Stable Horde — free community GPU network.
        Slower but reliable. No key needed (uses anonymous key).
        """
        try:
            print("Trying Stable Horde...")

            async with httpx.AsyncClient(timeout=30) as client:
                # Submit generation job
                submit_response = await client.post(
                    "https://stablehorde.net/api/v2/generate/async",
                    headers={
                        "apikey": "0000000000",  # Anonymous key
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": f"{prompt} ### {negative_prompt}",
                        "params": {
                            "width": 1024,
                            "height": 768,
                            "steps": 20,
                            "cfg_scale": 7.5,
                            "sampler_name": "k_euler",
                        },
                        "models": ["stable_diffusion"],
                        "r2": True,
                    }
                )

                if submit_response.status_code != 202:
                    print(f"Horde submit failed: {submit_response.status_code}")
                    return None

                job_id = submit_response.json().get("id")
                if not job_id:
                    return None

                print(f"Horde job submitted: {job_id}")

                # Poll for completion (max 3 minutes)
                for attempt in range(18):
                    await asyncio.sleep(10)

                    check_response = await client.get(
                        f"https://stablehorde.net/api/v2/generate/check/{job_id}"
                    )

                    if check_response.status_code != 200:
                        continue

                    check_data = check_response.json()
                    done = check_data.get("done", False)

                    if done:
                        # Get the result
                        status_response = await client.get(
                            f"https://stablehorde.net/api/v2/generate/status/{job_id}"
                        )
                        if status_response.status_code == 200:
                            generations = status_response.json().get(
                                "generations", []
                            )
                            if generations:
                                img_url = generations[0].get("img")
                                if img_url:
                                    print("✓ Image generated via Stable Horde")
                                    return {
                                        "job_id": job_id,
                                        "image_url": img_url,
                                        "status": "complete",
                                        "prompt_used": prompt,
                                        "method": "stable_horde"
                                    }
                        break

                    waited = (attempt + 1) * 10
                    print(f"Horde waiting... {waited}s")

                print("Horde timed out")
                return None

        except Exception as e:
            print(f"Stable Horde failed: {e}")
            return None

    def _get_fallback_image(self, room_type: str) -> dict:
        """
        Returns a curated high-quality interior photo.
        Used when all generation methods fail.
        """
        fallback_images = {
            "Living Room": (
                "https://images.unsplash.com/photo-1555041469-a586c61ea9bc"
                "?w=1024&q=80&fit=crop"
            ),
            "Bedroom": (
                "https://images.unsplash.com/photo-1616594039964-ae9021a400a0"
                "?w=1024&q=80&fit=crop"
            ),
            "Home Office": (
                "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89"
                "?w=1024&q=80&fit=crop"
            ),
            "Dining Room": (
                "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136"
                "?w=1024&q=80&fit=crop"
            ),
            "Studio Apartment": (
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688"
                "?w=1024&q=80&fit=crop"
            ),
        }

        image_url = fallback_images.get(
            room_type,
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc"
            "?w=1024&q=80&fit=crop"
        )

        return {
            "job_id": "fallback",
            "image_url": image_url,
            "status": "complete",
            "prompt_used": "fallback image",
            "method": "fallback"
        }

    async def check_status(self, job_id: str) -> dict:
        """Check status — jobs complete synchronously."""
        return {"job_id": job_id, "status": "complete"}


# Single instance
image_service = ImageGenerationService()