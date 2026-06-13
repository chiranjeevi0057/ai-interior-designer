# services/prompts.py
# Prompts optimized for smaller LLMs (llama3.2:1b)
# Shorter and more direct than full prompts.
# Groq/larger models also work well with these.

SYSTEM_PROMPT = """You are an expert interior designer. You generate complete room design plans in JSON format.

RULES:
1. Return ONLY valid JSON. No text before or after. No markdown. No backticks.
2. Never recommend furniture that cannot fit in the given room dimensions.
3. All costs must be in Indian Rupees reflecting current Indian market prices.
4. Every furniture item must have a specific placement and reasoning.
5. Stay within the specified budget."""


INITIAL_DESIGN_PROMPT = """Create an interior design plan for this room and return it as JSON.

ROOM:
- Type: {room_type}
- Size: {dimensions_summary}
- Light: {light_level}
- Style: {style_preference}
- Color Mood: {color_mood}
- Budget: {budget_range} INR
- Must have: {must_have_items}
- Avoid: {items_to_avoid}
- Notes: {special_constraints}

Return this exact JSON (fill in all values, no placeholders):

{{
  "session_id": "{session_id}",
  "version": 1,
  "room_type": "{room_type}",
  "room_dimensions_summary": "{dimensions_summary}",
  "spatial_observations": [
    "observation 1 about this specific room",
    "observation 2 about light in this room",
    "observation 3 about space usage"
  ],
  "recommended_theme": "{style_preference}",
  "theme_rationale": "2 sentences explaining why {style_preference} suits this {room_type}",
  "color_palette": [
    {{"name": "color name", "hex_code": "#XXXXXX", "usage": "wall color"}},
    {{"name": "color name", "hex_code": "#XXXXXX", "usage": "furniture color"}},
    {{"name": "color name", "hex_code": "#XXXXXX", "usage": "accent color"}},
    {{"name": "color name", "hex_code": "#XXXXXX", "usage": "trim color"}}
  ],
  "color_palette_notes": "why this palette works for {color_mood} mood",
  "furniture_plan": [
    {{
      "id": "item_1",
      "name": "Main Sofa",
      "category": "Seating",
      "recommended_dimensions": "200cm W x 85cm D x 80cm H",
      "placement": "Against the main wall, centered",
      "placement_reasoning": "Anchors the room and creates focal point",
      "priority": "essential",
      "estimated_cost_range": "15000-40000"
    }},
    {{
      "id": "item_2",
      "name": "Coffee Table",
      "category": "Tables",
      "recommended_dimensions": "110cm W x 55cm D x 45cm H",
      "placement": "Center of seating area, 45cm from sofa",
      "placement_reasoning": "Within easy reach from sofa, maintains traffic flow",
      "priority": "essential",
      "estimated_cost_range": "5000-15000"
    }},
    {{
      "id": "item_3",
      "name": "TV Unit",
      "category": "Storage",
      "recommended_dimensions": "150cm W x 40cm D x 50cm H",
      "placement": "Wall opposite to sofa",
      "placement_reasoning": "Optimal viewing distance and creates focal point",
      "priority": "essential",
      "estimated_cost_range": "8000-20000"
    }}
  ],
  "furniture_plan_notes": "overall layout strategy for this {room_type}",
  "traffic_flow_notes": "90cm clearance maintained on all main pathways",
  "lighting_plan": [
    {{
      "type": "Ambient",
      "description": "Ceiling LED panel light",
      "placement": "Center of ceiling",
      "reasoning": "Even base illumination across the room"
    }},
    {{
      "type": "Accent",
      "description": "Floor lamp with warm bulb",
      "placement": "Corner beside seating",
      "reasoning": "Creates warm reading corner and adds depth"
    }}
  ],
  "key_design_principles": [
    "Focal point established",
    "60-30-10 color rule applied",
    "Traffic flow maintained with 90cm clearance"
  ],
  "design_warnings": [],
  "budget_tier": "{budget_range}",
  "estimated_total_range": "35000-90000",
  "budget_notes": "Prioritise sofa and lighting first",
  "image_prompt_keywords": [
    "{room_type} interior",
    "{style_preference} style",
    "natural light",
    "professional interior photography",
    "8k quality"
  ],
  "style_descriptors": [
    "clean and functional",
    "well lit",
    "modern"
  ],
  "requires_visual_update": false,
  "visual_update_reason": null
}}"""


REFINEMENT_PROMPT = """Update this interior design plan based on the user request.

ROOM CONSTRAINTS (never change these):
{original_intake}

CURRENT PLAN (version {current_version}):
{current_plan}

USER REQUEST: "{user_message}"

Rules:
1. Only change what the user asked for
2. Keep all room dimensions and constraints
3. Set version to {next_version}
4. Set requires_visual_update to true if theme or major furniture changed
5. Return the COMPLETE updated plan as JSON only"""