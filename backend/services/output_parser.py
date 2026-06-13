# services/output_parser.py
# Parses and validates the LLM's JSON output.
# LLMs sometimes return slightly malformed JSON —
# this file handles those cases gracefully.

import json
import re
from typing import Optional
from models.design_plan import DesignPlan


class PlanOutputParser:
    """
    Extracts and validates a DesignPlan from raw LLM output.
    Handles common LLM formatting mistakes automatically.
    """

    def parse(self, raw_output: str, session_id: str) -> Optional[DesignPlan]:
        """
        Try to parse the LLM output into a DesignPlan.
        Returns None if parsing fails completely.
        """
        # Step 1: Clean the raw output
        cleaned = self._clean_output(raw_output)

        # Step 2: Try direct JSON parse
        data = self._try_parse_json(cleaned)

        # Step 3: If that fails, try to extract JSON from the text
        if data is None:
            data = self._extract_json_from_text(cleaned)

        # Step 4: If still None, return None (triggers retry)
        if data is None:
            return None

        # Step 5: Ensure session_id is correct
        data["session_id"] = session_id

        # Step 6: Validate with Pydantic
        try:
            return DesignPlan(**data)
        except Exception as e:
            print(f"Pydantic validation error: {e}")
            # Try to fix common field issues
            data = self._fix_common_issues(data)
            try:
                return DesignPlan(**data)
            except Exception as e2:
                print(f"Second validation error: {e2}")
                return None

    def _clean_output(self, text: str) -> str:
        """Remove common LLM formatting mistakes."""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Remove any text before the first {
        first_brace = text.find('{')
        if first_brace > 0:
            text = text[first_brace:]
        # Remove any text after the last }
        last_brace = text.rfind('}')
        if last_brace >= 0 and last_brace < len(text) - 1:
            text = text[:last_brace + 1]
        return text

    def _try_parse_json(self, text: str) -> Optional[dict]:
        """Try to parse as JSON directly."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    def _extract_json_from_text(self, text: str) -> Optional[dict]:
        """
        Try to find a JSON object within text.
        Handles cases where the LLM adds explanation around the JSON.
        """
        # Find all potential JSON objects
        pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(pattern, text, re.DOTALL)

        # Try each match, return the first valid one
        for match in matches:
            try:
                data = json.loads(match)
                # Check it looks like a design plan
                if "furniture_plan" in data or "recommended_theme" in data:
                    return data
            except json.JSONDecodeError:
                continue
        return None

    def _fix_common_issues(self, data: dict) -> dict:
        """Fix common issues that cause Pydantic validation to fail."""

        # Ensure required lists exist
        for field in ["spatial_observations", "color_palette", "furniture_plan",
                      "lighting_plan", "key_design_principles", "design_warnings",
                      "image_prompt_keywords", "style_descriptors"]:
            if field not in data or data[field] is None:
                data[field] = []

        # Ensure required strings exist
        for field in ["theme_rationale", "color_palette_notes", "furniture_plan_notes",
                      "traffic_flow_notes", "budget_tier", "estimated_total_range",
                      "budget_notes", "room_dimensions_summary"]:
            if field not in data or data[field] is None:
                data[field] = ""

        # Ensure version is an integer
        if "version" not in data or data["version"] is None:
            data["version"] = 1

        # Ensure requires_visual_update is boolean
        if "requires_visual_update" not in data:
            data["requires_visual_update"] = False

        # Fix recommended_theme if it doesn't match enum
        valid_themes = [
            "Minimalist", "Scandinavian", "Industrial", "Bohemian",
            "Contemporary", "Traditional", "Mid-Century Modern", "Japandi"
        ]
        if data.get("recommended_theme") not in valid_themes:
            data["recommended_theme"] = "Contemporary"

        # Fix furniture priority values
        valid_priorities = ["essential", "recommended", "optional"]
        for item in data.get("furniture_plan", []):
            if item.get("priority") not in valid_priorities:
                item["priority"] = "recommended"

        return data


# Single instance used throughout the app
output_parser = PlanOutputParser()