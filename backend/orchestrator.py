"""
Orchestrator - Routes queries to appropriate agents based on prompt type.
"""
from typing import Dict, Any, Optional
from agents.script_reviewer import evaluate_script
from agents.impact_agent import evaluate_impact


def route(content_text: str, prompt: Optional[str] = None, rubric_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Routes content, prompt, and rubric to the appropriate agent.
    
    Routing Logic:
    - If prompt contains impact/sensitivity keywords → Impact Agent
    - Otherwise → Script Reviewer (default for evaluative queries)
    
    Args:
        content_text: Combined script content from text_input and/or script_file
        prompt: Optional prompt/instruction from the user (renamed from question)
        rubric_text: Rubric/values text to evaluate against (default or user-provided)
        
    Returns:
        Dictionary with agent_used, summary, score, and details
    """
    # Normalize prompt for routing
    prompt_lower = (prompt or "").lower()
    
    # Keywords that indicate impact/sensitivity evaluation
    impact_keywords = [
        'impact', 'sensitivity', 'sensitive', 'social', 'cultural',
        'representation', 'diversity', 'inclusion', 'harmful', 'offensive',
        'appropriate', 'suitable', 'concerns', 'risks', 'ethical'
    ]
    
    # Check if prompt is about impact or sensitivity
    is_impact_query = any(keyword in prompt_lower for keyword in impact_keywords)
    
    # Route to appropriate agent with all parameters
    if is_impact_query:
        # Route to Impact Agent
        return evaluate_impact(content_text, prompt, rubric_text)
    else:
        # Default to Script Reviewer for evaluative queries
        return evaluate_script(content_text, prompt, rubric_text)

