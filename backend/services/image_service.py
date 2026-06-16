# services/image_service.py
# Generates concept renders using Stable Diffusion XL
# via HuggingFace Spaces Gradio API.
# Falls back gracefully if generation fails.

import asyncio
import httpx
import base64
import os
from typing import Optional
from models.design_plan import DesignPlan
from models.intake import IntakePayload
from services.prompt_synthesizer import prompt_synthesizer
from config import settings


class ImageGenerationService:
    """
    Handles image generation via HuggingFace Spaces.
    Uses SDXL-Lightning for fast generation on free GPU.
    """

    # Public HuggingFace Spaces that support SDXL
    # We try them in order until one works
    HF_SPACES = [
        "https://bytedance-sdxl-lightning.hf.space",
        "https://stabilityai-sdxl.hf.space",
    ]

    # Direct HuggingFace Inference API (uses your token)
    HF_INFERENCE_URL = (
        "https://api-inference.huggingface.co/models/"
        "stabilityai/stable-diffusion-xl-base-1.0"
    )

    def __init__(self):
        self.token = settings.huggingface_token
        print(f"✓ Image Service initialized")
        if self.token and self.token != "your_huggingface_token_here":
            print("  Using HuggingFace Inference API")
        else:
            print("  No HF token — will use public Spaces")

    async def generate_image(
        self,
        plan: DesignPlan,
        intake: IntakePayload
    ) -> dict:
        """
        Generate a concept render from the design plan.
        Tries multiple methods in order of preference.
        """
        # Build the optimized prompt
        prompt_data = prompt_synthesizer.synthesize(plan, intake)

        print(f"\n🎨 Generating image for session: {plan.session_id}")
        print(f"Prompt: {prompt_data['positive_prompt'][:150]}...")

        # Method 1: HuggingFace Inference API (if token available)
        if self.token and self.token != "your_huggingface_token_here":
            result = await self._generate_via_hf_api(prompt_data)
            if result:
                return result

        # Method 2: Try public Spaces via Gradio API
        result = await self._generate_via_gradio(prompt_data)
        if result:
            return result

        # Method 3: Fallback — return a curated placeholder
        print("All generation methods failed — using fallback image")
        return self._get_fallback_image(intake.room_type.value)

    async def _generate_via_hf_api(
        self,
        prompt_data: dict
    ) -> Optional[dict]:
        """
        Generate using HuggingFace Inference API.
        Requires a valid HF token.
        """
        try:
            print("Trying HuggingFace Inference API...")
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    self.HF_INFERENCE_URL,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt_data["positive_prompt"],
                        "parameters": {
                            "negative_prompt": prompt_data["negative_prompt"],
                            "width": 1024,
                            "height": 768,
                            "num_inference_steps": 25,
                            "guidance_scale": 7.5,
                        }
                    }
                )

                if response.status_code == 200:
                    # Response is raw image bytes
                    image_bytes = response.content
                    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                    image_url = f"data:image/jpeg;base64,{image_b64}"

                    print("✓ Image generated via HF Inference API")
                    return {
                        "job_id": f"hf-{prompt_data['positive_prompt'][:20]}",
                        "image_url": image_url,
                        "status": "complete",
                        "prompt_used": prompt_data["positive_prompt"],
                        "method": "hf_inference_api"
                    }
                elif response.status_code == 503:
                    # Model is loading — wait and retry once
                    print("Model loading, waiting 20 seconds...")
                    await asyncio.sleep(20)
                    response2 = await client.post(
                        self.HF_INFERENCE_URL,
                        headers={
                            "Authorization": f"Bearer {self.token}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "inputs": prompt_data["positive_prompt"],
                            "parameters": {
                                "negative_prompt": prompt_data["negative_prompt"],
                                "width": 1024,
                                "height": 768,
                                "num_inference_steps": 25,
                            }
                        }
                    )
                    if response2.status_code == 200:
                        image_bytes = response2.content
                        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                        image_url = f"data:image/jpeg;base64,{image_b64}"
                        print("✓ Image generated via HF Inference API (retry)")
                        return {
                            "job_id": "hf-retry",
                            "image_url": image_url,
                            "status": "complete",
                            "prompt_used": prompt_data["positive_prompt"],
                            "method": "hf_inference_api"
                        }
                else:
                    print(f"HF API error: {response.status_code} — {response.text[:200]}")
                    return None

        except Exception as e:
            print(f"HF Inference API failed: {e}")
            return None

    async def _generate_via_gradio(
        self,
        prompt_data: dict
    ) -> Optional[dict]:
        """
        Generate using public HuggingFace Spaces Gradio API.
        No token required.
        """
        try:
            print("Trying Gradio Space API...")
            from gradio_client import Client

            # Try SDXL-Lightning (fastest free SDXL)
            client = Client("ByteDance/SDXL-Lightning")

            result = await asyncio.to_thread(
                client.predict,
                prompt_data["positive_prompt"],  # prompt
                "1-Step",                         # num steps (fastest)
                api_name="/generate_image"
            )

            if result and isinstance(result, str):
                print(f"✓ Image generated via Gradio: {result[:50]}")
                return {
                    "job_id": "gradio-sdxl",
                    "image_url": result,
                    "status": "complete",
                    "prompt_used": prompt_data["positive_prompt"],
                    "method": "gradio_space"
                }

        except Exception as e:
            print(f"Gradio Space failed: {e}")

        return None

    def _get_fallback_image(self, room_type: str) -> dict:
        """
        Returns a curated real interior photo as fallback.
        These are high quality Unsplash photos of real rooms.
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
        """Check generation status — currently all jobs complete synchronously."""
        return {
            "job_id": job_id,
            "status": "complete"
        }


# Single instance
image_service = ImageGenerationService()