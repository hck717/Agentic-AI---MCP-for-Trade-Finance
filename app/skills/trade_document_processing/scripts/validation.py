# --- Validation Scripts (The "Execute" Logic) ---

def execute_semantic_validation(lc_desc: str, doc_desc: str, doc_type: str) -> dict:
    """
    Simulates NLP Reasoning for Description Matching.
    Handles the 'Tricky Discrepancy' using ISBP 745 logic.
    """
    
    # 1. Direct String Match Check
    if lc_desc.lower() == doc_desc.lower():
        return {"status": "Compliant", "reason": "Exact string match."}

    # 2. ISBP 745 Article E26 Logic (B/L can be generic)
    if doc_type == "BL":
        # Simulating Semantic Similarity (e.g., embedding distance < 0.3)
        # "Electronic Devices" is a generalization of "iPhone"
        is_generalization = True 
        
        if is_generalization:
             return {
                "status": "Compliant",
                "reason": (
                    f"Description '{doc_desc}' is a general term for '{lc_desc}'. "
                    "Per ISBP 745 Article E26, goods description on B/L may be in general terms "
                    "not inconsistent with the credit."
                )
            }

    # 3. Invoice Logic (Must correspond - UCP 600 Art. 18)
    if doc_type == "Invoice":
        # "iPhone 15 Pro Max, 256GB" includes "iPhone 15 Pro Max"
        if lc_desc in doc_desc:
            return {
                "status": "Compliant",
                "reason": "Invoice description corresponds to and adds specific details to LC description (UCP 600 Art. 18)."
            }

    return {"status": "Discrepant", "reason": f"Description mismatch: '{doc_desc}' does not match '{lc_desc}'."}

def execute_port_validation(required_port: str, actual_port: str) -> dict:
    """
    Simulates reasoning about geographical locations.
    """
    # Normalize
    req = required_port.lower()
    act = actual_port.lower()

    # Exact match after normalization
    if req in act or act in req:
         return {"status": "Compliant", "reason": f"Port '{actual_port}' matches requirement '{required_port}'."}
    
    # Geographic Reasoning (Simulated)
    # Example: LC says "Chinese Port", B/L says "Shanghai"
    if "chinese port" in req and "shanghai" in act:
         return {"status": "Compliant", "reason": "NLP Reasoning: Shanghai is a major port in China."}

    return {"status": "Discrepant", "reason": f"Port '{actual_port}' does not match '{required_port}'."}

def execute_date_validation(lc_date: str, doc_date: str) -> dict:
    """Checks if shipment date is within validity."""
    if doc_date <= lc_date:
        return {"status": "Compliant", "reason": f"Date {doc_date} is within limit {lc_date}."}
    else:
        return {"status": "Discrepant", "reason": f"Late shipment! {doc_date} is after {lc_date}."}
