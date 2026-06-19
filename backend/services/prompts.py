# services/prompts.py
# Prompts engineered for room-type accuracy.
# Room type is repeated explicitly multiple times
# to prevent the model from defaulting to generic furniture.

SYSTEM_PROMPT = """You are an expert interior designer specializing in Indian homes. You generate precise, room-specific interior design plans in JSON format.

CRITICAL RULES:
1. Return ONLY valid JSON. No text before or after. No markdown. No backticks.
2. ALWAYS design specifically for the EXACT room type given. Never substitute furniture from other room types.
3. A HOME OFFICE needs: desk, office chair, storage, monitor setup. NOT sofas or TV units.
4. A BEDROOM needs: bed, wardrobe, side tables, dresser. NOT sofas or dining tables.
5. A LIVING ROOM needs: sofa, coffee table, TV unit. NOT desks or beds.
6. A DINING ROOM needs: dining table, dining chairs, sideboard. NOT sofas or beds.
7. A STUDIO APARTMENT needs: multifunctional furniture that serves sleeping, living and working.
8. Never recommend furniture that cannot physically fit in the given dimensions.
9. All costs must be in Indian Rupees with realistic Indian market prices.
10. Stay strictly within the specified budget."""


INITIAL_DESIGN_PROMPT = """Design a {room_type} interior. This is a {room_type} — not a living room, not a bedroom — specifically a {room_type}.

ROOM DETAILS:
- Room Type: {room_type} (IMPORTANT: design specifically for a {room_type})
- Dimensions: {dimensions_summary}
- Natural Light: {light_level}
- Preferred Style: {style_preference}
- Color Mood: {color_mood}
- Budget: {budget_range} INR
- Must Include: {must_have_items}
- Avoid: {items_to_avoid}
- Special Notes: {special_constraints}

FURNITURE GUIDE FOR THIS SPECIFIC ROOM TYPE:
{room_furniture_guide}

Return ONLY this JSON with no other text. Fill every field with specific, accurate values:

{{
  "session_id": "{session_id}",
  "version": 1,
  "room_type": "{room_type}",
  "room_dimensions_summary": "{dimensions_summary}",
  "spatial_observations": [
    "specific observation about {room_type} usage in this space",
    "observation about how {light_level} light affects this {room_type}",
    "observation about furniture arrangement given {dimensions_summary}"
  ],
  "recommended_theme": "{style_preference}",
  "theme_rationale": "2 sentences explaining exactly why {style_preference} suits this {room_type} given {light_level} light and {dimensions_summary} dimensions",
  "color_palette": [
    {{"name": "specific color name", "hex_code": "#XXXXXX", "usage": "primary wall color for {room_type}"}},
    {{"name": "specific color name", "hex_code": "#XXXXXX", "usage": "main furniture color"}},
    {{"name": "specific color name", "hex_code": "#XXXXXX", "usage": "accent color"}},
    {{"name": "specific color name", "hex_code": "#XXXXXX", "usage": "trim and detail color"}}
  ],
  "color_palette_notes": "why this {color_mood} palette suits this {room_type}",
  "furniture_plan": [
    {furniture_items_placeholder}
  ],
  "furniture_plan_notes": "overall layout strategy specific to this {room_type}",
  "traffic_flow_notes": "how people move through this {room_type} with this layout",
  "lighting_plan": [
    {{
      "type": "Ambient",
      "description": "specific ceiling light suitable for a {room_type}",
      "placement": "center of ceiling",
      "reasoning": "provides base illumination for {room_type} activities"
    }},
    {{
      "type": "Task",
      "description": "specific task light for {room_type} activities",
      "placement": "specific position relevant to {room_type}",
      "reasoning": "supports primary activities in a {room_type}"
    }}
  ],
  "key_design_principles": [
    "principle specifically applied to this {room_type} layout",
    "principle about {style_preference} style in this {room_type}",
    "principle about optimizing {room_type} functionality"
  ],
  "design_warnings": [],
  "budget_tier": "{budget_range}",
  "estimated_total_range": "realistic range in INR for this {room_type}",
  "budget_notes": "budget advice specific to furnishing a {room_type} in India",
  "image_prompt_keywords": [
    "{room_type} interior",
    "{style_preference} {room_type}",
    "{room_type} furniture",
    "{light_level} natural light",
    "{color_mood} color scheme",
    "professional {room_type} photography"
  ],
  "style_descriptors": [
    "{style_preference} aesthetic",
    "{color_mood} mood",
    "functional {room_type}"
  ],
  "requires_visual_update": false,
  "visual_update_reason": null
}}"""


# Room-specific furniture guides injected into the prompt
ROOM_FURNITURE_GUIDES = {
    "Living Room": """
LIVING ROOM FURNITURE (use these, not bedroom or office furniture):
- Primary seating: 2-seater or 3-seater sofa (essential)
- Coffee table: centered in front of sofa (essential)
- TV unit: on wall opposite sofa (essential)
- Optional: accent chair, side tables, bookshelf, area rug
- DO NOT include: beds, desks, dining tables, office chairs""",

    "Bedroom": """
BEDROOM FURNITURE (use these, not living room or office furniture):
- Bed: queen or king size with headboard (essential)
- Wardrobe: for clothing storage (essential)
- Side tables: one or two beside bed (essential)
- Optional: dresser, study corner with small desk, floor lamp
- DO NOT include: sofas, TV units, dining tables, office setups""",

    "Home Office": """
HOME OFFICE FURNITURE (use these, not living room or bedroom furniture):
- Study desk / work desk: large enough for monitor and work (essential)
- Ergonomic office chair: with lumbar support (essential)
- Bookshelf or storage unit: for files and books (essential)
- Optional: small sofa or accent chair for reading, whiteboard
- DO NOT include: beds, sofas, coffee tables, TV units, dining furniture""",

    "Dining Room": """
DINING ROOM FURNITURE (use these, not living room or bedroom furniture):
- Dining table: sized for the family (essential)
- Dining chairs: matching set (essential)
- Sideboard or buffet: for crockery storage (essential)
- Optional: display cabinet, bar trolley, pendant lighting
- DO NOT include: sofas, beds, TV units, office desks""",

    "Studio Apartment": """
STUDIO APARTMENT FURNITURE (multifunctional pieces that serve multiple purposes):
- Sofa bed or murphy bed: sleeping and seating combined (essential)
- Compact dining table with foldable chairs (essential)
- Wardrobe with integrated study nook if possible (essential)
- Optional: room divider, compact kitchen island, wall shelves
- Focus on space-saving, multifunctional furniture throughout""",
}


REFINEMENT_PROMPT = """Update this {room_type} interior design plan based on the user's request.

ORIGINAL ROOM (never change these constraints):
{original_intake}

CURRENT {room_type} DESIGN PLAN (version {current_version}):
{current_plan}

CONVERSATION HISTORY:
{conversation_history}

USER REQUEST: "{user_message}"

RULES:
1. This is a {room_type} — keep all furniture appropriate for a {room_type}
2. Only change what the user explicitly requested
3. Keep room dimensions, budget tier, and room type unchanged
4. Set version to {next_version}
5. Set requires_visual_update to true if theme, style, major furniture, or colors changed
6. Set requires_visual_update to false for minor text changes only
7. Return the COMPLETE updated plan as valid JSON only — no other text"""