"""
Data schemas for request/response models.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class QueryRequest(BaseModel):
    """Request model for the /query endpoint."""
    text_input: Optional[str] = None
    question: Optional[str] = None
    # Note: file is handled separately via multipart/form-data


class AgentResponse(BaseModel):
    """Response model from agents."""
    agent_used: str
    summary: str
    score: float  # 0.0 to 1.0
    details: Dict[str, Any]


class QueryResponse(BaseModel):
    """Final response model for the /query endpoint."""
    agent_used: str
    summary: str
    score: float
    details: Dict[str, Any]

