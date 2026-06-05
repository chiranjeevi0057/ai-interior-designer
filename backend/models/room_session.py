# room_session.py
# Defines the room_sessions table in PostgreSQL.
# Each row = one user's complete design session.

from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from database import Base

class RoomSession(Base):
    
    # The actual table name in PostgreSQL
    __tablename__ = "room_sessions"
    
    # PRIMARY KEY
    # Unique ID for each session (we generate this as a UUID string)
    id = Column(String, primary_key=True, index=True)
    
    # USER INPUT
    # Stores the complete intake form data as JSON
    # Example: {"room_type": "Living Room", "length": 14, "width": 12, ...}
    intake_data = Column(JSON, nullable=False)
    
    # DESIGN PLAN
    # Stores the complete AI-generated design plan as JSON
    # This is the full DesignPlan schema from Phase 5
    design_plan = Column(JSON, nullable=True)
    
    # Which version of the plan this is (increments with each refinement)
    plan_version = Column(Integer, default=1)
    
    # CONVERSATION HISTORY
    # Stores the full conversation as a JSON array
    # Example: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    conversation_history = Column(JSON, default=list)
    
    # IMAGE GENERATION
    # ID of the image generation job on HuggingFace
    image_job_id = Column(String, nullable=True)
    
    # URL of the generated image
    image_url = Column(Text, nullable=True)
    
    # Current status of image generation
    # Values: "pending", "generating", "complete", "failed"
    image_status = Column(String, default="pending")
    
    # The prompt we sent to SDXL (useful for debugging)
    image_prompt = Column(Text, nullable=True)
    
    # SESSION STATE
    # Current state of the overall session
    # Values: "idle", "planning", "plan_ready", "image_generating", 
    #         "complete", "failed"
    session_state = Column(String, default="idle")
    
    # Whether this session is still active
    is_active = Column(Boolean, default=True)
    
    # TIMESTAMPS
    # Automatically set when the row is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Automatically updated every time the row changes
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # When the session expires
    expires_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<RoomSession id={self.id} state={self.session_state}>"