# Phase 2: Multi-Agent System with MCP & LangGraph 🧠

This document details the implementation of the **Plan-and-Execute** architecture for the Trade Finance Compliance Agent.

## 🏗️ Architecture: The "Brain" and the "Skills"

We use a **ReAct** (Reasoning + Acting) approach tailored for Trade Finance:

### 1. The Skills (MCP Tools)
Located in `app/mcp/skills.py`. These are the atomic capabilities:

- **Pick (Data Extraction):**
  - `pick_lc_data(pdf)`: Standardized output via `LCData` schema.
  - `pick_invoice_data(pdf)`: Standardized output via `InvoiceData` schema.
  - `pick_bl_data(pdf)`: Standardized output via `BLData` schema.

- **Execute (Reasoning & Validation):**
  - `execute_semantic_validation()`: The "Tricky Discrepancy" solver. Uses NLP logic to handle "iPhone" vs "Electronic Goods" (ISBP 745 Art. E26).
  - `execute_port_validation()`: Geographic reasoning (e.g., Shanghai == Chinese Port).
  - `execute_date_validation()`: Mathematical date comparison.

### 2. The Brain (LangGraph)
Located in `app/agents/graph.py`. This orchestrates the workflow:

**The Flow:**
1.  **Planner Node:**
    - Input: Raw documents.
    - Thought: "I need to check the critical fields defined in the LC."
    - Output: A `plan` (list of checks) and extracted data in state.

2.  **B/L Expert Node:**
    - Input: `LCData`, `BLData`.
    - Action: Calls `execute_port_validation`, `execute_semantic_validation`.
    - Output: Validation results for the B/L.

3.  **Invoice Expert Node:**
    - Input: `LCData`, `InvoiceData`.
    - Action: Calls `execute_semantic_validation` (stricter rules), Check Amount.
    - Output: Validation results for the Invoice.

4.  **Reviewer Node:**
    - Input: All validation results.
    - Logic: UCP 600 Art. 14 (Conflict Check).
    - Output: Final Verdict ("Compliant" or "Discrepant") + Reasoning.

## 🚀 How to Run the POC

### Prerequisites
```bash
pip install langgraph pydantic
```

### Running the Agent
We have provided a main entry point that mocks the full lifecycle using the "Apple iPhone Import" dataset:

```bash
python -m app.main
```

### Expected Output
The system will demonstrate the "Tricky Discrepancy" handling:

```text
🚀 Starting Trade Finance Agent System (POC)...
==================================================
--- 🧠 Planner: Analyzing Documents ---
--- 🚢 Agent 1 (B/L Expert): Checking Logistics ---
--- 💰 Agent 2 (Invoice Expert): Checking Financials ---
--- ⚖️ Agent 3 (Reviewer): Finalizing Verdict ---

==================================================
🏁 FINAL VERDICT: Compliant
📝 REASONING: All documents consistent with LC terms and UCP 600.
==================================================

🔍 Detailed Validation Results:
✅ [B/L] Port Loading: Port 'Los Angeles Port' matches requirement 'Los Angeles'.
✅ [B/L] Shipment Date: Date 2026-04-25 is within limit 2026-05-01.
✅ [B/L] Goods Description: Description 'Electronic Devices - Apple iPhone' is a general term for 'Apple iPhone 15 Pro Max smartphones'. Per ISBP 745 Article E26, goods description on B/L may be in general terms not inconsistent with the credit.
✅ [Invoice] Goods Description: Invoice description corresponds to and adds specific details to LC description (UCP 600 Art. 18).
✅ [Invoice] Amount: Amount within limit.
```

## 🛠️ Key Technical Features

1.  **Standardized Schemas (`app/models/schemas.py`):**
    - Uses Pydantic to ensure all agents speak the same "language" (MCP Protocol).
    
2.  **Logic Encapsulation (`app/mcp/skills.py`):**
    - Separation of concerns: The *Graph* manages state, the *Skills* handle logic.
    - Easy to swap mock skills for real OCR/LLM calls later.

3.  **Context-Aware Validation:**
    - The `execute_semantic_validation` function behaves differently depending on `doc_type` (B/L vs Invoice), mirroring the actual UCP 600 rules.
