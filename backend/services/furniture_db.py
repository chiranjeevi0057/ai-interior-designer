# services/furniture_db.py
# Curated furniture database with Indian market pricing.
# Used to enrich AI recommendations with specific product details,
# price ranges, and shopping links.

from typing import List, Dict, Optional
from pydantic import BaseModel


class FurnitureProduct(BaseModel):
    id: str
    name: str
    category: str
    style_tags: List[str]       # Styles this item suits
    min_price: int              # Minimum price in INR
    max_price: int              # Maximum price in INR
    dimensions: str             # Standard dimensions
    material: str               # Primary material
    description: str            # Short description
    buy_links: List[Dict]       # Shopping links
    suitable_rooms: List[str]   # Room types this suits
    budget_tiers: List[str]     # Which budget tiers this fits


# ── Furniture Database ────────────────────────────────────────
FURNITURE_DATABASE: List[FurnitureProduct] = [

    # ── SOFAS ─────────────────────────────────────────────────
    FurnitureProduct(
        id="sofa_001",
        name="3-Seater Fabric Sofa",
        category="Seating",
        style_tags=["Contemporary", "Scandinavian", "Minimalist"],
        min_price=15000,
        max_price=35000,
        dimensions="210cm W x 85cm D x 80cm H",
        material="Fabric upholstery, wooden legs",
        description="Clean-lined fabric sofa with solid wood legs, ideal for modern living rooms",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/sofas.html"},
            {"store": "Urban Ladder", "url": "https://www.urbanladder.com/sofas"},
        ],
        suitable_rooms=["Living Room", "Studio Apartment"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    FurnitureProduct(
        id="sofa_002",
        name="L-Shaped Sectional Sofa",
        category="Seating",
        style_tags=["Contemporary", "Bohemian", "Traditional"],
        min_price=35000,
        max_price=90000,
        dimensions="270cm W x 180cm D x 85cm H",
        material="Premium fabric, engineered wood frame",
        description="Spacious L-shaped sectional perfect for large living rooms",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/sofas.html"},
            {"store": "IKEA", "url": "https://www.ikea.com/in/en/cat/sofas-fu003/"},
        ],
        suitable_rooms=["Living Room"],
        budget_tiers=["50000 to 150000", "150000 to 400000"]
    ),

    FurnitureProduct(
        id="sofa_003",
        name="2-Seater Loveseat",
        category="Seating",
        style_tags=["Minimalist", "Scandinavian", "Japandi"],
        min_price=12000,
        max_price=25000,
        dimensions="150cm W x 80cm D x 78cm H",
        material="Linen fabric, solid wood legs",
        description="Compact loveseat ideal for small rooms and studio apartments",
        buy_links=[
            {"store": "Urban Ladder", "url": "https://www.urbanladder.com/sofas"},
            {"store": "Wooden Street", "url": "https://www.woodenstreet.com/sofas"},
        ],
        suitable_rooms=["Living Room", "Studio Apartment", "Bedroom"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    # ── COFFEE TABLES ─────────────────────────────────────────
    FurnitureProduct(
        id="table_001",
        name="Solid Wood Coffee Table",
        category="Tables",
        style_tags=["Scandinavian", "Traditional", "Mid-Century Modern"],
        min_price=5000,
        max_price=18000,
        dimensions="120cm W x 60cm D x 45cm H",
        material="Solid sheesham wood",
        description="Natural wood coffee table with clean lines and durable finish",
        buy_links=[
            {"store": "Wooden Street", "url": "https://www.woodenstreet.com/coffee-tables"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/coffee-tables.html"},
        ],
        suitable_rooms=["Living Room"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    FurnitureProduct(
        id="table_002",
        name="Glass Top Coffee Table",
        category="Tables",
        style_tags=["Contemporary", "Minimalist", "Industrial"],
        min_price=8000,
        max_price=22000,
        dimensions="110cm W x 55cm D x 45cm H",
        material="Tempered glass, metal frame",
        description="Modern glass coffee table that makes small spaces feel larger",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/coffee-tables.html"},
            {"store": "HomeTown", "url": "https://www.hometown.in/furniture/tables"},
        ],
        suitable_rooms=["Living Room", "Studio Apartment"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    # ── TV UNITS ──────────────────────────────────────────────
    FurnitureProduct(
        id="tv_001",
        name="Wall-Mounted TV Unit",
        category="Storage",
        style_tags=["Minimalist", "Contemporary", "Scandinavian"],
        min_price=8000,
        max_price=20000,
        dimensions="150cm W x 35cm D x 45cm H",
        material="Engineered wood, matte finish",
        description="Floating TV unit that saves floor space and looks modern",
        buy_links=[
            {"store": "Urban Ladder", "url": "https://www.urbanladder.com/tv-units"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/tv-units.html"},
        ],
        suitable_rooms=["Living Room", "Bedroom"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    FurnitureProduct(
        id="tv_002",
        name="Solid Wood TV Cabinet",
        category="Storage",
        style_tags=["Traditional", "Bohemian", "Mid-Century Modern"],
        min_price=15000,
        max_price=40000,
        dimensions="180cm W x 45cm D x 55cm H",
        material="Solid sheesham wood",
        description="Spacious wooden TV cabinet with storage drawers",
        buy_links=[
            {"store": "Wooden Street", "url": "https://www.woodenstreet.com/tv-units"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/tv-units.html"},
        ],
        suitable_rooms=["Living Room"],
        budget_tiers=["50000 to 150000", "150000 to 400000"]
    ),

    # ── BEDS ──────────────────────────────────────────────────
    FurnitureProduct(
        id="bed_001",
        name="Queen Size Platform Bed",
        category="Beds",
        style_tags=["Minimalist", "Scandinavian", "Contemporary"],
        min_price=18000,
        max_price=45000,
        dimensions="160cm W x 200cm L x 35cm H",
        material="Engineered wood, fabric headboard",
        description="Low-profile platform bed with upholstered headboard",
        buy_links=[
            {"store": "Urban Ladder", "url": "https://www.urbanladder.com/beds"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/beds.html"},
        ],
        suitable_rooms=["Bedroom"],
        budget_tiers=["50000 to 150000", "150000 to 400000"]
    ),

    FurnitureProduct(
        id="bed_002",
        name="King Size Wooden Bed",
        category="Beds",
        style_tags=["Traditional", "Bohemian", "Mid-Century Modern"],
        min_price=25000,
        max_price=70000,
        dimensions="180cm W x 200cm L x 120cm H",
        material="Solid sheesham wood",
        description="Classic wooden bed with ornate headboard and storage",
        buy_links=[
            {"store": "Wooden Street", "url": "https://www.woodenstreet.com/beds"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/beds.html"},
        ],
        suitable_rooms=["Bedroom"],
        budget_tiers=["50000 to 150000", "150000 to 400000", "Above 400000"]
    ),

    # ── WARDROBES ─────────────────────────────────────────────
    FurnitureProduct(
        id="wardrobe_001",
        name="3-Door Sliding Wardrobe",
        category="Storage",
        style_tags=["Contemporary", "Minimalist", "Scandinavian"],
        min_price=20000,
        max_price=55000,
        dimensions="180cm W x 60cm D x 210cm H",
        material="Engineered wood, mirror doors",
        description="Space-saving sliding wardrobe with mirror panels",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/wardrobes.html"},
            {"store": "HomeTown", "url": "https://www.hometown.in/furniture/wardrobes"},
        ],
        suitable_rooms=["Bedroom", "Studio Apartment"],
        budget_tiers=["50000 to 150000", "150000 to 400000"]
    ),

    # ── DINING ────────────────────────────────────────────────
    FurnitureProduct(
        id="dining_001",
        name="4-Seater Dining Set",
        category="Dining",
        style_tags=["Contemporary", "Scandinavian", "Minimalist"],
        min_price=15000,
        max_price=35000,
        dimensions="120cm W x 75cm D x 76cm H",
        material="Engineered wood table, fabric chairs",
        description="Compact dining set perfect for small families",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/dining-sets.html"},
            {"store": "Urban Ladder", "url": "https://www.urbanladder.com/dining-tables"},
        ],
        suitable_rooms=["Dining Room", "Studio Apartment"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    FurnitureProduct(
        id="dining_002",
        name="6-Seater Solid Wood Dining Set",
        category="Dining",
        style_tags=["Traditional", "Bohemian", "Mid-Century Modern"],
        min_price=30000,
        max_price=80000,
        dimensions="180cm W x 90cm D x 76cm H",
        material="Solid sheesham wood",
        description="Classic wooden dining set for larger families",
        buy_links=[
            {"store": "Wooden Street", "url": "https://www.woodenstreet.com/dining-sets"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/dining-sets.html"},
        ],
        suitable_rooms=["Dining Room"],
        budget_tiers=["50000 to 150000", "150000 to 400000"]
    ),

    # ── STUDY/OFFICE ──────────────────────────────────────────
    FurnitureProduct(
        id="desk_001",
        name="Study Desk with Shelves",
        category="Work",
        style_tags=["Minimalist", "Contemporary", "Scandinavian"],
        min_price=6000,
        max_price=18000,
        dimensions="120cm W x 55cm D x 75cm H",
        material="Engineered wood",
        description="Compact study desk with built-in shelving",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/study-tables.html"},
            {"store": "IKEA", "url": "https://www.ikea.com/in/en/cat/desks-fu002/"},
        ],
        suitable_rooms=["Home Office", "Bedroom", "Studio Apartment"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    FurnitureProduct(
        id="chair_001",
        name="Ergonomic Office Chair",
        category="Seating",
        style_tags=["Contemporary", "Minimalist", "Industrial"],
        min_price=8000,
        max_price=25000,
        dimensions="65cm W x 65cm D x 110cm H",
        material="Mesh back, padded seat",
        description="Ergonomic chair with lumbar support for long work sessions",
        buy_links=[
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/office-chairs.html"},
            {"store": "Amazon", "url": "https://www.amazon.in/office-chairs"},
        ],
        suitable_rooms=["Home Office", "Studio Apartment"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),

    # ── ACCENT CHAIRS ─────────────────────────────────────────
    FurnitureProduct(
        id="accent_001",
        name="Accent Armchair",
        category="Seating",
        style_tags=["Bohemian", "Mid-Century Modern", "Contemporary"],
        min_price=8000,
        max_price=22000,
        dimensions="75cm W x 78cm D x 85cm H",
        material="Velvet upholstery, metal legs",
        description="Statement armchair that adds personality to any room",
        buy_links=[
            {"store": "Urban Ladder", "url": "https://www.urbanladder.com/chairs"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/chairs.html"},
        ],
        suitable_rooms=["Living Room", "Bedroom"],
        budget_tiers=["50000 to 150000", "150000 to 400000"]
    ),

    # ── BOOKSHELVES ───────────────────────────────────────────
    FurnitureProduct(
        id="shelf_001",
        name="5-Tier Bookshelf",
        category="Storage",
        style_tags=["Minimalist", "Industrial", "Scandinavian"],
        min_price=4000,
        max_price=15000,
        dimensions="80cm W x 30cm D x 180cm H",
        material="Engineered wood, metal frame",
        description="Tall bookshelf for books, plants and display items",
        buy_links=[
            {"store": "IKEA", "url": "https://www.ikea.com/in/en/cat/bookcases-shelving-units-10791/"},
            {"store": "Pepperfry", "url": "https://www.pepperfry.com/bookshelves.html"},
        ],
        suitable_rooms=["Living Room", "Home Office", "Bedroom"],
        budget_tiers=["Under 50000", "50000 to 150000"]
    ),
]


class FurnitureRecommender:
    """
    Matches AI-generated furniture plan items with
    real products from the database.
    """

    def get_recommendations(
        self,
        furniture_items: list,
        style: str,
        budget_tier: str,
        room_type: str
    ) -> List[Dict]:
        """
        For each furniture item in the AI plan, find matching
        products from the database.
        """
        recommendations = []

        for item in furniture_items:
            matches = self._find_matches(
                item_name=item.name,
                category=item.category,
                style=style,
                budget_tier=budget_tier,
                room_type=room_type
            )

            recommendations.append({
                "ai_item": {
                    "name": item.name,
                    "placement": item.placement,
                    "reasoning": item.placement_reasoning,
                    "priority": item.priority,
                    "estimated_cost": item.estimated_cost_range,
                },
                "products": [p.model_dump() for p in matches[:2]]
            })

        return recommendations

    def _find_matches(
        self,
        item_name: str,
        category: str,
        style: str,
        budget_tier: str,
        room_type: str
    ) -> List[FurnitureProduct]:
        """Find matching products from the database."""
        matches = []

        item_lower = item_name.lower()

        for product in FURNITURE_DATABASE:
            score = 0

            # Category match
            if product.category.lower() == category.lower():
                score += 3

            # Name keyword match
            keywords = item_lower.split()
            for keyword in keywords:
                if keyword in product.name.lower():
                    score += 2

            # Style match
            if style in product.style_tags:
                score += 2

            # Budget tier match
            if budget_tier in product.budget_tiers:
                score += 2

            # Room match
            if room_type in product.suitable_rooms:
                score += 1

            if score >= 3:
                matches.append((score, product))

        # Sort by score and return products
        matches.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in matches[:3]]

    def get_budget_summary(
        self,
        recommendations: List[Dict]
    ) -> Dict:
        """Calculate budget summary from recommendations."""
        total_min = 0
        total_max = 0
        essential_min = 0
        essential_max = 0

        for rec in recommendations:
            if rec["products"]:
                product = rec["products"][0]
                total_min += product["min_price"]
                total_max += product["max_price"]
                if rec["ai_item"]["priority"] == "essential":
                    essential_min += product["min_price"]
                    essential_max += product["max_price"]

        return {
            "total_min": total_min,
            "total_max": total_max,
            "essential_min": essential_min,
            "essential_max": essential_max,
            "total_range": f"₹{total_min:,} – ₹{total_max:,}",
            "essential_range": f"₹{essential_min:,} – ₹{essential_max:,}",
        }


# Single instance
furniture_recommender = FurnitureRecommender()