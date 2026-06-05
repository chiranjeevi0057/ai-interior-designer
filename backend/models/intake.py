# intake.py
# Validates the intake form data sent from the frontend.
# returns an error before it even reaches our code.

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class RoomType(str, Enum):
    LIVING_ROOM = "Living Room"
    BEDROOM = "Bedroom"
    HOME_OFFICE = "Home Office"
    DINING_ROOM = "Dining Room"
    STUDIO_APARTMENT = "Studio Apartment"

class StylePreference(str, Enum):
    MINIMALIST = "Minimalist"
    SCANDINAVIAN = "Scandinavian"
    INDUSTRIAL = "Industrial"
    BOHEMIAN = "Bohemian"
    CONTEMPORARY = "Contemporary"
    TRADITIONAL = "Traditional"
    MID_CENTURY_MODERN = "Mid-Century Modern"
    JAPANDI = "Japandi"

class ColorMood(str, Enum):
    WARM_COZY = "Warm and Cozy"
    COOL_CALM = "Cool and Calm"
    BOLD_VIBRANT = "Bold and Vibrant"
    NEUTRAL_CLEAN = "Neutral and Clean"

class LightLevel(str, Enum):
    BRIGHT = "Bright"
    MODERATE = "Moderate"
    LOW = "Low"

class BudgetRange(str, Enum):
    UNDER_50K = "Under 50000"
    RANGE_50K_150K = "50000 to 150000"
    RANGE_150K_400K = "150000 to 400000"
    ABOVE_400K = "Above 400000"

class DimensionUnit(str, Enum):
    FEET = "feet"
    METERS = "meters"

class IntakePayload(BaseModel):
    
    # Room basics
    room_type: RoomType
    length: float = Field(gt=0, description="Room length")
    width: float = Field(gt=0, description="Room width")
    ceiling_height: float = Field(gt=0, description="Ceiling height")
    unit: DimensionUnit = DimensionUnit.FEET
    
    # Style preferences
    style_preference: StylePreference
    color_mood: ColorMood
    light_level: LightLevel
    
    # Constraints
    budget_range: BudgetRange
    must_have_items: List[str] = Field(
        default=[],
        description="Furniture items the user must have"
    )
    items_to_avoid: Optional[str] = Field(
        default=None,
        description="Things the user does not want"
    )
    special_constraints: Optional[str] = Field(
        default=None,
        description="Special notes like door positions"
    )
    
    # Dimension validation
    @validator("length", "width")
    def validate_room_size(cls, v, field):
        if v < 6:
            raise ValueError(
                f"{field.name} seems too small. "
                f"Minimum room dimension is 6 feet / 2 meters."
            )
        if v > 100:
            raise ValueError(
                f"{field.name} seems too large. "
                f"Please check your dimensions."
            )
        return v
    
    @validator("ceiling_height")
    def validate_ceiling(cls, v):
        if v < 7:
            raise ValueError(
                "Ceiling height below 7 feet is very unusual. "
                "Please check your measurement."
            )
        return v
    
    def get_area(self) -> float:
        return round(self.length * self.width, 2)
    
    def get_dimensions_summary(self) -> str:
        unit_short = "ft" if self.unit == DimensionUnit.FEET else "m"
        area = self.get_area()
        return (
            f"{self.length}{unit_short} × {self.width}{unit_short} × "
            f"{self.ceiling_height}{unit_short} ceiling "
            f"({area} sq {unit_short})"
        )