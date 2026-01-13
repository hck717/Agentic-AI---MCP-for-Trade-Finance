from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.models.schemas import AgentState, LCData, InvoiceData, BLData, PackingListData

# IMPORT FROM NEW SKILLS STRUCTURE
from app.skills.trade_document_processing.scripts.extraction import (
    pick_lc_data,
    pick_invoice_data,
    pick_bl_data,
    pick_packing_list_data,
)
from app.skills.trade_document_processing.scripts.validation import (
    execute_semantic_validation,
    execute_port_validation,
    execute_date_validation,
    execute_weight_validation,
)
from app.skills.finalize_compliance.scripts.finalize_compliance import (
    finalize_compliance_from_results,
)

# REFERENCING UTILITY
from app.utils.referencing import generate_professional_report


# --- Node 1: Planner (The "Plan" Step) ---

def planner_node(state: AgentState):
    """Analyze LC requirements and create a plan."""
    print(f"--- 🧠 Planner: Analyzing Documents for Scenario: {state.scenario_id} ---")

    # Action: Pick Data (Simulated retrieval with scenario_id)
    sid = state.scenario_id
    lc = pick_lc_data("mock/lc.md", sid)
    inv = pick_invoice_data("mock/inv.md", sid)
    bl = pick_bl_data("mock/bl.md", sid)
    pl = pick_packing_list_data("mock/pl.md", sid)

    # Initialize Evidence Map
    evidence_map = {
        "E1": f"Letter of Credit ({sid})",
        "E2": f"Commercial Invoice ({sid})",
        "E3": f"Bill of Lading ({sid})",
        "E4": f"Packing List ({sid})",
    }

    # Generate Plan
    plan = [
        "Check Port of Loading",
        "Check Latest Shipment Date",
        "Check Goods Description (Invoice)",
        "Check Goods Description (B/L)",
        "Check Packing List Weight vs B/L",
    ]

    return {
        "lc_data": lc,
        "invoice_data": inv,
        "bl_data": bl,
        "packing_list_data": pl,
        "plan": plan,
        "evidence_map": evidence_map,
    }


# --- Node 2: B/L Expert (The "Execute" Step) ---

def bl_expert_node(state: AgentState):
    """Agent 1: Checks Bill of Lading details."""
    print("--- 🚢 Agent 1 (B/L Expert): Checking Logistics ---")
    lc = state.lc_data
    bl = state.bl_data
    results = []

    # Check 1: Port Validation
    port_check = execute_port_validation(lc.port_of_loading, bl.port_of_loading)
    results.append({"check": "Port Loading", "doc": "B/L", "evidence_ids": ["E1", "E3"], **port_check})

    # Check 2: Date Validation
    date_check = execute_date_validation(lc.latest_shipment_date, bl.shipped_on_board_date)
    results.append({"check": "Shipment Date", "doc": "B/L", "evidence_ids": ["E1", "E3"], **date_check})

    # Check 3: Description Validation
    desc_check = execute_semantic_validation(
        lc.goods_description, bl.goods_description, "BL"
    )
    results.append({"check": "Goods Description", "doc": "B/L", "evidence_ids": ["E1", "E3"], **desc_check})

    return {"validation_results": state.validation_results + results}


# --- Node 3: Invoice Expert (The "Execute" Step) ---

def invoice_expert_node(state: AgentState):
    """Agent 2: Checks Commercial Invoice details."""
    print("--- 💰 Agent 2 (Invoice Expert): Checking Financials ---")
    lc = state.lc_data
    inv = state.invoice_data
    results = []

    # Check 1: Description Validation
    desc_check = execute_semantic_validation(
        lc.goods_description, inv.goods_description, "Invoice"
    )
    results.append({"check": "Goods Description", "doc": "Invoice", "evidence_ids": ["E1", "E2"], **desc_check})

    # Check 2: Amount
    if inv.amount <= lc.amount:
        res = {"status": "Compliant", "reason": "Amount within limit."}
    else:
        res = {"status": "Discrepant", "reason": "Overdrawn amount."}
    results.append({"check": "Amount", "doc": "Invoice", "evidence_ids": ["E1", "E2"], **res})

    return {"validation_results": state.validation_results + results}


# --- Node 4: Packing List Expert (The "Execute" Step) ---

def packing_list_expert_node(state: AgentState):
    """Agent 3: Checks Packing List details and cross-checks."""
    print("--- 📦 Agent 3 (PL Expert): Checking Cargo Details ---")
    lc = state.lc_data
    pl = state.packing_list_data
    bl = state.bl_data
    results = []

    # Check 1: Description
    desc_check = execute_semantic_validation(
        lc.goods_description, pl.goods_description, "PackingList"
    )
    results.append({"check": "Goods Description", "doc": "PackingList", "evidence_ids": ["E1", "E4"], **desc_check})

    # Check 2: Weight Cross-Check (PL vs B/L)
    weight_check = execute_weight_validation(bl.gross_weight, pl.gross_weight)
    results.append(
        {"check": "Gross Weight (vs B/L)", "doc": "PackingList", "evidence_ids": ["E3", "E4"], **weight_check}
    )

    return {"validation_results": state.validation_results + results}


# --- Node 5: Reviewer (The "Synthesize" Step via Agent Skill) ---

def reviewer_node(state: AgentState):
    """Agent 4: Uses the finalize_compliance Agent Skill to produce a verdict."""
    print("--- ⚖️ Agent 4 (Reviewer): Finalizing Verdict via Agent Skill ---")

    # Call original compliance skill (Minimal logic change)
    summary = finalize_compliance_from_results(state.validation_results)

    # Generate Professional Report with Evidence Appendix (New Referencing Function)
    professional_report = generate_professional_report(
        final_verdict=summary["final_verdict"],
        reasoning=summary["reasoning"],
        validation_results=state.validation_results,
        evidence_map=state.evidence_map
    )

    return {
        "final_verdict": summary["final_verdict"],
        "reasoning": professional_report, # Update reasoning with professional markdown
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
