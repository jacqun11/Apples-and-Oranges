"""
Impact Agent - Evaluates content for social impact and sensitivity.
Returns mock evaluation results for prototype purposes.
"""
from typing import Dict, Any


def evaluate_impact(content: str, prompt: str = None, rubric_text: str = None) -> Dict[str, Any]:
    """
    Evaluates content for social impact, sensitivity, and potential concerns.
    
    Args:
        content: The content to evaluate
        prompt: Optional prompt/instruction from the user
        rubric_text: Optional rubric/values text to evaluate against
        
    Returns:
        Dictionary with agent_used, summary, score, and details
    """
    # Note: rubric_text is available for future use with real AI agents
    # Currently using mock evaluation logic
    # Mock evaluation logic
    # In production, this would call an LLM or specialized impact analysis service
    
    content_lower = content.lower()
    
    # Check for sensitive topics (mock detection)
    sensitive_topics = {
        'violence': ['violence', 'violent', 'fight', 'attack', 'war'],
        'discrimination': ['discrimination', 'prejudice', 'bias', 'stereotype'],
        'sensitive_content': ['trauma', 'abuse', 'harassment', 'exploitation']
    }
    
    detected_topics = []
    for topic, keywords in sensitive_topics.items():
        if any(kw in content_lower for kw in keywords):
            detected_topics.append(topic)
    
    # Calculate impact score (higher = more positive impact, lower = more concerns)
    base_score = 0.7
    
    # Adjust score based on detected topics
    if detected_topics:
        score_adjustment = -0.2 * len(detected_topics)
        base_score = max(0.2, base_score + score_adjustment)
    
    # Check for positive impact indicators
    positive_indicators = ['diversity', 'inclusion', 'empowerment', 'representation', 'awareness']
    positive_count = sum(1 for ind in positive_indicators if ind in content_lower)
    base_score = min(0.95, base_score + (positive_count * 0.05))
    
    final_score = round(base_score, 2)
    
    # Generate mock assessment
    if final_score >= 0.7:
        impact_level = "Positive"
        concerns = "Minimal concerns. Content appears to handle sensitive topics thoughtfully."
        recommendations = "Continue current approach. Consider adding trigger warnings if needed."
    elif final_score >= 0.5:
        impact_level = "Mixed"
        concerns = "Some sensitive content detected. Review for potential unintended harm."
        recommendations = "Consider sensitivity review and potential content warnings."
    else:
        impact_level = "Needs Review"
        concerns = "Multiple sensitive topics identified. Requires careful evaluation."
        recommendations = "Strongly recommend sensitivity review and content modification."
    
    return {
        "agent_used": "impact_agent",
        "summary": f"Impact evaluation completed. Detected {len(detected_topics)} sensitive topic categories. Impact level: {impact_level.lower()}.",
        "score": final_score,
        "details": {
            "impact_level": impact_level,
            "concerns": concerns,
            "recommendations": recommendations,
            "detected_topics": detected_topics if detected_topics else ["None detected"],
            "evaluation_notes": "This is a mock evaluation. In production, this would include detailed impact analysis from an AI agent."
        }
    }

