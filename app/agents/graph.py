from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.models.schemas import AgentState, LCData, InvoiceData, BLData, PackingListData

# IMPORT FROM NEW SKILLS STRUCTURE
from app.skills.trade_document_processing.scripts.extraction import (
    pick_lc_data, pick_invoice_data, pick_bl_data, pick_packing_list_data
)
from app.skills.trade_document_processing.scripts.validation import (
    execute_semantic_validation, execute_port_validation, execute_date_validation, execute_weight_validation
)

# --- Node 1: Planner (The "Plan" Step) ---
def planner_node(state: AgentState):
    """
    Analyzes the LC requirements and creates a plan.
    Thinking: "I need to check if the B/L port matches the LC and if the Invoice description matches."
    """
    print(f"--- 🧠 Planner: Analyzing Documents for Scenario: {state.scenario_id} ---")
    
    # Action: Pick Data (Simulated retrieval with scenario_id)
    sid = state.scenario_id
    lc = pick_lc_data("mock/lc.md", sid)
    inv = pick_invoice_data("mock/inv.md", sid)
    bl = pick_bl_data("mock/bl.md", sid)
    pl = pick_packing_list_data("mock/pl.md", sid)
    
    # Generate Plan
    plan = [
        "Check Port of Loading",
        "Check Latest Shipment Date",
        "Check Goods Description (Invoice)",
        "Check Goods Description (B/L)",
        "Check Packing List Weight vs B/L"
    ]
    
    return {
        "lc_data": lc,
        "invoice_data": inv,
        "bl_data": bl,
        "packing_list_data": pl,
        "plan": plan
    }

# --- Node 2: BL Expert (The "Execute" Step) ---
def bl_expert_node(state: AgentState):
    """
    Agent 1: Checks Bill of Lading details.
    """
    print("--- 🚢 Agent 1 (B/L Expert): Checking Logistics ---")
    lc = state.lc_data
    bl = state.bl_data
    results = []
    
    # Check 1: Port Validation (Logic/Reasoning)
    port_check = execute_port_validation(lc.port_of_loading, bl.port_of_loading)
    results.append({"check": "Port Loading", "doc": "B/L", **port_check})
    
    # Check 2: Date Validation
    date_check = execute_date_validation(lc.latest_shipment_date, bl.shipped_on_board_date)
    results.append({"check": "Shipment Date", "doc": "B/L", **date_check})
    
    # Check 3: Description Validation (Tricky Case: Generic Term)
    desc_check = execute_semantic_validation(lc.goods_description, bl.goods_description, "BL")
    results.append({"check": "Goods Description", "doc": "B/L", **desc_check})

    return {"validation_results": state.validation_results + results}

# --- Node 3: Invoice Expert (The "Execute" Step) ---
def invoice_expert_node(state: AgentState):
    """
    Agent 2: Checks Commercial Invoice details.
    """
    print("--- 💰 Agent 2 (Invoice Expert): Checking Financials ---")
    lc = state.lc_data
    inv = state.invoice_data
    results = []
    
    # Check 1: Description Validation (Specific Term)
    desc_check = execute_semantic_validation(lc.goods_description, inv.goods_description, "Invoice")
    results.append({"check": "Goods Description", "doc": "Invoice", **desc_check})
    
    # Check 2: Amount (Simple math)
    if inv.amount <= lc.amount:
        res = {"status": "Compliant", "reason": "Amount within limit."}
    else:
        res = {"status": "Discrepant", "reason": "Overdrawn amount."}
    results.append({"check": "Amount", "doc": "Invoice", **res})

    return {"validation_results": state.validation_results + results}

# --- Node 4: Packing List Expert (The "Execute" Step) ---
def packing_list_expert_node(state: AgentState):
    """
    Agent 3: Checks Packing List details and Cross-Checks.
    """
    print("--- 📦 Agent 3 (PL Expert): Checking Cargo Details ---")
    lc = state.lc_data
    pl = state.packing_list_data
    bl = state.bl_data
    results = []
    
    # Check 1: Description
    desc_check = execute_semantic_validation(lc.goods_description, pl.goods_description, "PackingList")
    results.append({"check": "Goods Description", "doc": "PackingList", **desc_check})
    
    # Check 2: Weight Cross-Check (PL vs B/L)
    weight_check = execute_weight_validation(bl.gross_weight, pl.gross_weight)
    results.append({"check": "Gross Weight (vs B/L)", "doc": "PackingList", **weight_check})

    return {"validation_results": state.validation_results + results}

# --- Node 5: Reviewer (The "Synthesize" Step) ---
def reviewer_node(state: AgentState):
    """
    Agent 4: Synthesizes results and checks for conflicts (UCP 600 Art 14).
    """
    print("--- ⚖️ Agent 4 (Reviewer): Finalizing Verdict ---")
    
    discrepancies = [r for r in state.validation_results if r["status"] == "Discrepant"]
    
    if not discrepancies:
        verdict = "Compliant"
        reason = "All documents (LC, Invoice, B/L, Packing List) consistent with terms and UCP 600."
    else:
        verdict = "Discrepant"
        reason = f"Found {len(discrepancies)} discrepancies: " + "; ".join([d["reason"] for d in discrepancies])
        
    return {
        "final_verdict": verdict,
        "reasoning": reason
    }

# --- Graph Definition ---
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("bl_expert", bl_expert_node)
    workflow.add_node("invoice_expert", invoice_expert_node)
    workflow.add_node("packing_list_expert", packing_list_expert_node)
    workflow.add_node("reviewer", reviewer_node)
    
    # Define Edges (The Flow)
    workflow.set_entry_point("planner")
    
    # Flow: Planner -> BL -> Invoice -> PL -> Reviewer
    workflow.add_edge("planner", "bl_expert")
    workflow.add_edge("bl_expert", "invoice_expert")
    workflow.add_edge("invoice_expert", "packing_list_expert")
    workflow.add_edge("packing_list_expert", "reviewer")
    workflow.add_edge("reviewer", END)
    
    return workflow.compile()
