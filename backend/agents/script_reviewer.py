"""
Script Reviewer Agent - Evaluates creative scripts and content.
Returns mock evaluation results for prototype purposes.
"""
from typing import Dict, Any


def evaluate_script(content: str, prompt: str = None, rubric_text: str = None) -> Dict[str, Any]:
    """
    Evaluates a script and returns structured feedback.
    
    Args:
        content: The script content to evaluate
        prompt: Optional prompt/instruction from the user
        rubric_text: Optional rubric/values text to evaluate against
        
    Returns:
        Dictionary with agent_used, summary, score, and details
    """
    # Note: rubric_text is available for future use with real AI agents
    # Currently using mock evaluation logic
    # Mock evaluation logic
    # In production, this would call an LLM or evaluation service
    
    # Simple heuristic: longer content gets slightly higher scores
    content_length = len(content)
    base_score = min(0.5 + (content_length / 2000) * 0.3, 0.95)
    
    # Adjust based on keywords (mock logic)
    positive_keywords = ['creative', 'innovative', 'compelling', 'engaging', 'unique']
    negative_keywords = ['generic', 'boring', 'unclear', 'confusing']
    
    positive_count = sum(1 for kw in positive_keywords if kw.lower() in content.lower())
    negative_count = sum(1 for kw in negative_keywords if kw.lower() in content.lower())
    
    score_adjustment = (positive_count * 0.05) - (negative_count * 0.1)
    final_score = max(0.1, min(0.95, base_score + score_adjustment))
    
    # Generate mock verdict
    if final_score >= 0.7:
        verdict = "Good fit"
        risks = "Minor concerns about pacing in the middle section."
        benefits = "Strong narrative structure with compelling character development."
    elif final_score >= 0.5:
        verdict = "Needs revision"
        risks = "Some structural issues and unclear character motivations."
        benefits = "Solid concept with potential for improvement."
    else:
        verdict = "Requires significant work"
        risks = "Multiple structural and narrative issues identified."
        benefits = "Core idea has potential but needs substantial development."
    
    return {
        "agent_used": "script_reviewer",
        "summary": f"Script evaluation completed. Content length: {content_length} characters. Overall assessment: {verdict.lower()}.",
        "score": round(final_score, 2),
        "details": {
            "verdict": verdict,
            "risks": risks,
            "benefits": benefits,
            "content_length": content_length,
            "evaluation_notes": "This is a mock evaluation. In production, this would include detailed analysis from an AI agent."
        }
    }

