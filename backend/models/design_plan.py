# design_plan.py
# This is the CORE DATA CONTRACT of the entire application.
# The image generator reads this structure to create prompts.

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RoomTheme(str, Enum):
    MINIMALIST = "Minimalist"
    SCANDINAVIAN = "Scandinavian"
    INDUSTRIAL = "Industrial"
    BOHEMIAN = "Bohemian"
    CONTEMPORARY = "Contemporary"
    TRADITIONAL = "Traditional"
    MID_CENTURY_MODERN = "Mid-Century Modern"
    JAPANDI = "Japandi"

class ColorSwatch(BaseModel):
    name: str = Field(description="Color name e.g. Warm Ivory")
    hex_code: str = Field(description="Hex color code e.g. #F5F0E8")
    usage: str = Field(description="How this color is used e.g. Primary wall color")

class FurnitureItem(BaseModel):
    id: str = Field(description="Unique ID e.g. item_1")
    name: str = Field(description="Furniture name e.g. 3-Seater Sofa")
    category: str = Field(description="Category e.g. Seating, Storage, Tables")
    recommended_dimensions: str = Field(description="e.g. 220cm W x 90cm D x 85cm H")
    placement: str = Field(description="Where to place it e.g. Against the north wall")
    placement_reasoning: str = Field(description="Why this placement works")
    priority: str = Field(description="essential, recommended, or optional")
    estimated_cost_range: str = Field(description="Cost in Indian Rupees e.g. 15000-35000")

class LightingItem(BaseModel):
    type: str = Field(description="Ambient, Task, or Accent")
    description: str = Field(description="What kind of light fixture")
    placement: str = Field(description="Where to place it")
    reasoning: str = Field(description="Why this lighting choice works")

class DesignPlan(BaseModel):
    
    # Session tracking
    session_id: str
    version: int = Field(default=1, description="Increments with each refinement")
    
    # Room understanding
    room_type: str
    room_dimensions_summary: str = Field(
        description="e.g. 14ft x 12ft x 9ft ceiling (168 sq ft)"
    )
    spatial_observations: List[str] = Field(
        description="Key observations about the space"
    )
    
    # Theme
    recommended_theme: RoomTheme
    theme_rationale: str = Field(
        description="2-3 sentences explaining why this theme suits this room"
    )
    
    # Colors
    color_palette: List[ColorSwatch] = Field(
        description="4-5 color swatches for this design"
    )
    color_palette_notes: str = Field(
        description="Overall reasoning for the color palette"
    )
    
    # Furniture
    furniture_plan: List[FurnitureItem] = Field(
        description="4-8 furniture pieces with placement"
    )
    furniture_plan_notes: str = Field(
        description="Overall furniture layout strategy"
    )
    traffic_flow_notes: str = Field(
        description="How people move through the space"
    )
    
    # Lighting
    lighting_plan: List[LightingItem] = Field(
        description="2-4 lighting recommendations"
    )
    
    # Design guidance
    key_design_principles: List[str] = Field(
        description="3-5 design principles applied to this room"
    )
    design_warnings: List[str] = Field(
        default=[],
        description="Things to avoid or watch out for"
    )
    
    # Budget
    budget_tier: str = Field(description="The selected budget range")
    estimated_total_range: str = Field(
        description="Total estimated cost range in INR"
    )
    budget_notes: str = Field(
        description="Budget allocation advice"
    )
    
    # Image generation helpers
    image_prompt_keywords: List[str] = Field(
        description="8-12 keywords for SDXL image generation"
    )
    style_descriptors: List[str] = Field(
        description="4-6 visual mood descriptors"
    )
    
    # Controls whether a new image should be generated
    requires_visual_update: bool = Field(default=False)
    visual_update_reason: Optional[str] = Field(default=None)