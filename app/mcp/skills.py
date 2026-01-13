import math
from app.models.schemas import LCData, InvoiceData, BLData

# --- Skill 1: Pick (Data Extraction) ---
# In a real MCP server, these would use OCR/LLM extraction.
# Here we mock them for the POC demo using Dataset 1 (Apple Import).

def pick_lc_data(file_path: str) -> LCData:
    """Extracts structured data from the Letter of Credit."""
    # Mocking extraction from 'mock_documents/1_APPLE_IPHONE_IMPORT/LC_LC-2026-001-HSBC.md'
    return LCData(
        lc_number="LC-2026-001-HSBC",
        amount=500000.00,
        currency="USD",
        expiry_date="2026-05-20",
        port_of_loading="Los Angeles",
        port_of_discharge="Hong Kong",
        latest_shipment_date="2026-05-01",
        goods_description="Apple iPhone 15 Pro Max smartphones",
        beneficiary="Apple Distribution International",
        applicant="TechWorld Distribution Ltd",
        incoterms="CIF"
    )

def pick_invoice_data(file_path: str) -> InvoiceData:
    """Extracts structured data from the Commercial Invoice."""
    # Mocking extraction from 'mock_documents/1_APPLE_IPHONE_IMPORT/INVOICE_INV-2026-00145.md'
    return InvoiceData(
        invoice_number="INV-2026-00145",
        amount=500000.00,
        currency="USD",
        goods_description="Apple iPhone 15 Pro Max, 256GB, Space Black", # Specific
        buyer="TechWorld Distribution Ltd",
        seller="Apple Distribution International"
    )

def pick_bl_data(file_path: str) -> BLData:
    """Extracts structured data from the Bill of Lading."""
    # Mocking extraction from 'mock_documents/1_APPLE_IPHONE_IMPORT/BL_MAEU123456789.md'
    return BLData(
        bl_number="MAEU123456789",
        port_of_loading="Los Angeles Port",
        port_of_discharge="Hong Kong Port",
        shipped_on_board_date="2026-04-25",
        goods_description="Electronic Devices - Apple iPhone", # Generic (ISBP 745 Art. E26)
        carrier="Maersk Line"
    )

# --- Skill 2: Execute (Reasoning & Validation) ---

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
