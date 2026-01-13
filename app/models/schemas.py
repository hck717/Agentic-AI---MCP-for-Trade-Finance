from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

# --- 1. Standardized Document Inputs (MCP Input) ---

class TradeDocument(BaseModel):
    """Base class for all trade documents"""
    file_path: str = Field(..., description="Path to the document file")
    doc_type: Literal["LC", "Invoice", "BL", "PackingList"]

class LCData(BaseModel):
    """Structured Data Extracted from Letter of Credit"""
    lc_number: str
    amount: float
    currency: str
    expiry_date: str
    port_of_loading: str
    port_of_discharge: str
    latest_shipment_date: str
    goods_description: str
    beneficiary: str
    applicant: str
    incoterms: str

class InvoiceData(BaseModel):
    """Structured Data Extracted from Commercial Invoice"""
    invoice_number: str
    amount: float
    currency: str
    goods_description: str
    buyer: str
    seller: str

class BLData(BaseModel):
    """Structured Data Extracted from Bill of Lading"""
    bl_number: str
    port_of_loading: str
    port_of_discharge: str
    shipped_on_board_date: str
    goods_description: str
    carrier: str
    gross_weight: str

class PackingListData(BaseModel):
    """Structured Data Extracted from Packing List"""
    pl_number: str
    goods_description: str
    gross_weight: str
    net_weight: str
    total_packages: str

# --- 2. Agent State (LangGraph State) ---

class AgentState(BaseModel):
    """The shared state of the Multi-Agent System"""
    scenario_id: str = "apple"
    ollama_url: str = "http://localhost:11434/v1" # New: Dynamic LLM URL
    
    lc_data: Optional[LCData] = None
    invoice_data: Optional[InvoiceData] = None
    bl_data: Optional[BLData] = None
    packing_list_data: Optional[PackingListData] = None
    
    # The Plan (List of checks to perform)
    plan: List[str] = Field(default_factory=list)
    
    # Results from Agents
    validation_results: List[dict] = Field(default_factory=list)
    
    # Referencing & Appendix
    evidence_map: Dict[str, str] = Field(default_factory=dict, description="Maps ID (E1) to Source Description")
    
    # Final Verdict
    final_verdict: Optional[Literal["Compliant", "Discrepant"]] = None
    reasoning: str = ""
    
    # Chat Context
    chat_history: List[dict] = Field(default_factory=list)
