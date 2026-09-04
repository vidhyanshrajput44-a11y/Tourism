"""
Photo Verification Logic for Heritage Rewards.
Includes a lightweight heuristic / pretrained mockup check and a force_verify flag.
"""

from typing import Tuple

def verify_monument_photo(image_file_name: str, claimed_monument_id: str, force_verify: bool = False) -> Tuple[bool, float, str]:
    """
    This is a plausibility check, not true per-monument recognition - 
    production version would use a fine-tuned classifier per heritage site.
    
    Here, we conceptually run a pretrained image classifier. If force_verify is True, 
    we automatically succeed (useful for hackathon live demos).
    """
    if force_verify:
        return True, 0.95, "Force verified for demo purposes."

    # Conceptual heuristic check on filename to simulate basic CV filtering
    # In reality, this would pass the image bytes to a CNN/CLIP model.
    lower_name = image_file_name.lower()
    
    # Reject obvious non-architectural/monument photos based on fake heuristic
    if "selfie" in lower_name or "face" in lower_name:
        return False, 0.12, "Image appears to be a selfie or portrait, not a monument."
    if "food" in lower_name or "menu" in lower_name:
        return False, 0.05, "Image appears to be food/indoor, not an outdoor monument."
        
    # By default, accept it as plausible architecture
    # Simulate a confidence score
    return True, 0.88, "Plausible architectural landmark detected."

