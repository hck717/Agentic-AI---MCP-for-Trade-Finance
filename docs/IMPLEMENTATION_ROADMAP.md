# Trade Finance Agentic AI - Implementation Roadmap

**Status:** Phase 1 Complete ✅ | Phase 2 Ready to Start 🚀

**Created:** 2026-01-13 (Tuesday, 3:17 PM HKT)

---

## Overview

This document outlines the complete implementation roadmap for building an **Agentic AI system for Trade Finance LC Compliance** using LangGraph, Claude Opus, and MCP tools.

### Three Core Components

1. **PICK Strategy** - Data extraction & entity selection logic
2. **REVIEW Strategy** - Compliance validation & decision making (In Progress)
3. **RESPONSE Strategy** - Output formatting & reporting (In Progress)

### Current Status

- ✅ **PICK Strategy Documented** - [docs/PICK_STRATEGY.md](../docs/PICK_STRATEGY.md)
- ✅ **LC Reference Complete** - [docs/LC_TYPES_DETAILS_PARTIES.md](../docs/LC_TYPES_DETAILS_PARTIES.md)
- ✅ **Mock Datasets Created** - [mock_documents/](../mock_documents/README.md)
- ⏳ **MCP Tools Implementation** - Next Phase
- ⏳ **LangGraph Workflow** - Next Phase
- ⏳ **Integration Testing** - Next Phase

---

## Phase 1: Research & Documentation ✅ COMPLETE

### What Was Delivered

#### 1. PICK Strategy Document
**File:** [docs/PICK_STRATEGY.md](../docs/PICK_STRATEGY.md)

**Contents:**
- Part 1: Data Hierarchy (Tier 1/2/3 fields)
- Part 2: Extraction Strategy (4-step extraction process)
- Part 3: Decision Tree (5-phase validation flow)
- Part 4: Why This Approach Works (explanation & examples)
- Part 5: Implementation Checklist (MCP tools to build)

**Key Insights:**
- **Tier 1 Fields:** Amount, currency, dates, parties (blocking issues)
- **Tier 2 Fields:** Special conditions, required documents, insurance
- **Tier 3 Fields:** Supporting data (audit trail, logistics)
- **Semantic Matching:** Use embeddings (text-embedding-3-small) for description hierarchy
- **ISBP 745 Rules:** B/L can use generic descriptions per Art. E26

**Critical Problem Solved:**
```
OLD (Flat OCR):
  Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black"
  B/L: "Electronic Devices"
  String Match: FAIL ✗
  
NEW (Semantic + ISBP 745):
  Embedding Similarity: 0.72 (below 0.85 threshold BUT)
  ISBP 745 Art. E26: "B/L descriptions may be generic"
  Hierarchy Check: Specific-to-Generic is acceptable
  Result: COMPLIANT ✓
```

---

#### 2. LC Types & Details Reference
**File:** [docs/LC_TYPES_DETAILS_PARTIES.md](../docs/LC_TYPES_DETAILS_PARTIES.md)

**Contents:**
- Part 1: LC Types Classification (6 categories)
  - By revocability (irrevocable vs revocable)
  - By confirmation (confirmed vs unconfirmed)
  - By presentation (sight vs time/usance)
  - By coverage (full vs revolving)
  - By transferability (transferable vs non-transferable)
  - By payment source (documentary vs stand-by)

- Part 2: LC Structural Details (23 essential fields)
  - Field 20 (Reference Number)
  - Field 31 (Issue/Expiry Dates)
  - Field 32 (Amount & Tolerance)
  - Field 43 (Form of Credit)
  - Field 44 (Form of Payment)
  - Field 46 (Documents Required)
  - Field 47 (Special Conditions)
  - Field 50 (Applicant)
  - Field 59 (Beneficiary)
  - + Incoterms, Ports, Shipping Terms

- Part 3: LC Parties (7 party types)
  - **Primary:** Applicant (buyer), Beneficiary (seller)
  - **Banking:** Issuing Bank, Confirming Bank, Negotiating Bank
  - **Supporting:** Inspector, Insurance Company, Shipping Line

- Part 4: Compliance Checklist
  - Tier 1 (Critical): Expiry, Currency, Amount, Quantity, Shipment Date, Ports, Parties
  - Tier 2 (Important): Documents, Special Conditions, Descriptions, Cross-References

---

#### 3. Mock Trade Finance Datasets
**Folder:** [mock_documents/](../mock_documents/)

**3 Complete Transaction Sets (12 Documents Total):**

| Dataset | Company | Sector | LC Amount | Currency | Tests |
|---------|---------|--------|-----------|----------|-------|
| **1_APPLE_IPHONE** | TechWorld Distribution | Electronics Retail (Large) | USD 500,000 | USD | Description hierarchy, large qty, multi-SKU |
| **2_TEXTILE_EXPORT** | Vietnamese Silk Trading | Textile Mfg (SME) | EUR 85,000 | EUR | Special conditions, origin cert, pre-shipment inspection |
| **3_AUTOMOTIVE_PARTS** | Precision Mfg India | Auto Parts (Mid-size) | AUD 250,000 | AUD | Quality cert, transhipment restriction, tolerance bands |

**Each dataset includes:**
1. **Letter of Credit** - Full LC with all fields, parties, conditions
2. **Commercial Invoice** - Multi-item invoice with totals
3. **Bill of Lading** - Shipping document with vessel, ports, cargo details
4. **Packing List** - Package-level contents, weights, carton ranges

**Total Documentation:**
- 12 markdown files (4 docs × 3 datasets)
- ~50KB of realistic trade finance data
- Ready for PDF conversion
- Covers different currencies, commodities, company sizes, sectors

**Compliance Testing Scenarios:**

**Dataset 1 (Apple):**
```
TC Description Matching
  LC: "Apple iPhone 15 Pro Max smartphones"
  Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black" (specific)
  B/L: "Electronic Devices - Apple iPhone" (generic)
  
  Test: Does system recognize acceptable hierarchy?
  Expected: COMPLIANT (per ISBP 745 Art. E26)
```

**Dataset 2 (Textile):**
```
Special Conditions Verification
  LC Conditions:
    - Pre-shipment inspection mandatory
    - Certificate of Origin (Vietnam) required
    - 100% payment on B/L presentation
    
  Test: Are all conditions satisfied in documents?
  Expected: Flag missing pre-shipment inspection if not attached
```

**Dataset 3 (Automotive):**
```
Restriction Enforcement
  LC Condition: "Transhipment NOT allowed"
  B/L Status: No transhipment notation (direct Chennai -> Melbourne)
  
  Test: Does system detect transhipment restriction?
  Expected: COMPLIANT (no transhipment found)
```

---

### Resources Created

**Documentation Files:**
1. [docs/PICK_STRATEGY.md](../docs/PICK_STRATEGY.md) - 17.7 KB
2. [docs/LC_TYPES_DETAILS_PARTIES.md](../docs/LC_TYPES_DETAILS_PARTIES.md) - 24.2 KB
3. [mock_documents/README.md](../mock_documents/README.md) - 12.3 KB

**Mock Document Files:**
- 12 markdown files in 3 datasets (Apple, Textile, Automotive)
- All stored in [mock_documents/](../mock_documents/)
- Ready for PDF conversion

**Total Size:** ~60-70 KB of documentation + mock data

---

## Phase 2: MCP Tools Implementation ⏳ READY TO START

### What to Build

#### Priority 1: Core Extraction Tools

**Tool 1: `extract_lc_requirements(lc_pdf_path)`**
```python
"""
Extract all LC requirements from PDF/text

Input: Path to LC document (PDF or markdown)
Output: Structured dict with:
  - lc_number, issue_date, expiry_date
  - amount, currency, tolerance_plus, tolerance_minus
  - applicant (name, address)
  - beneficiary (name, address)
  - goods_description, quantity, unit_price
  - latest_shipment_date
  - port_of_loading, port_of_discharge
  - incoterms
  - required_documents (list)
  - special_conditions (list)

Tech: OCR (for PDF) + NLP for field extraction
Model: Claude + regex for structured output
Error Handling: Partial extraction + confidence scores
"""
```

**Tool 2: `extract_invoice_details(invoice_pdf_path)`**
```python
"""
Extract invoice items, amounts, parties

Input: Path to Commercial Invoice
Output: Structured dict with:
  - invoice_number, date
  - seller_name, seller_address
  - buyer_name, buyer_address
  - items[] with description, quantity, unit_price, total
  - subtotal, tax, total_amount
  - currency
  - reference_lc

Tech: Table parsing + NLP for text extraction
Validation: Currency consistency, amount sum check
"""
```

**Tool 3: `extract_bl_details(bl_pdf_path)`**
```python
"""
Extract B/L shipping & cargo details

Input: Path to Bill of Lading
Output: Structured dict with:
  - bl_number, on_board_date
  - shipper, consignee, notify_party
  - vessel_name, voyage_number
  - port_of_loading, port_of_discharge
  - goods_description (general/specific as written)
  - quantity_description
  - number_of_packages, gross_weight, net_weight
  - freight_charges, freight_payment
  - reference documents (invoice #, lc #)

Tech: OCR + structured field extraction
Special: Preserve description as-is (for semantic matching later)
"""
```

**Tool 4: `extract_packing_list_details(packing_list_pdf_path)`**
```python
"""
Extract package-level contents & logistics

Input: Path to Packing List
Output: Structured dict with:
  - packing_list_number, date
  - invoice_number, bl_number (cross-references)
  - items[] with carton_range, description, quantity, weight
  - total_cartons, total_weight

Tech: Table parsing for carton-by-carton breakdown
Validation: Cross-check with B/L quantities
"""
```

---

#### Priority 2: Semantic Matching Tools

**Tool 5: `semantic_similarity(text1: str, text2: str) -> float`**
```python
"""
Compute semantic similarity between descriptions

Input: Two text strings (e.g., invoice desc vs B/L desc)
Output: Similarity score 0.0-1.0

Logic:
  1. Use text-embedding-3-small to embed both
  2. Compute cosine similarity
  3. Return score
  
Example:
  similarity("Apple iPhone 15 Pro Max 256GB", "Electronic Devices")
  → 0.72 (below 0.85 exact match threshold)
  
Usage: Determine if descriptions acceptably match
"""
```

**Tool 6: `apply_isbp745_rules(lc_desc, invoice_desc, bl_desc) -> bool`**
```python
"""
Apply ISBP 745 rules to description hierarchy

Input: Three descriptions (LC baseline, invoice specific, B/L generic)
Output: Boolean whether hierarchy is acceptable

Rules:
  1. Invoice can be MORE specific than LC ✓
  2. B/L can be generic (per ISBP 745 Art. E26) ✓
  3. If invoice specific AND B/L generic → OK ✓
  4. If all three match semantic similarity > 0.70 → OK ✓
  5. If B/L is completely unrelated → DISCREPANCY ✗

Example:
  LC: "Apple iPhone smartphones"
  Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black"
  B/L: "Electronic Devices"
  → apply_isbp745_rules() returns True (acceptable hierarchy)
"""
```

---

#### Priority 3: Validation Tools

**Tool 7: `validate_tier1_checks(lc_data, invoice_data, bl_data) -> list[Discrepancy]`**
```python
"""
Perform all Tier 1 (critical) validation checks

Checks:
  1. Currency Match [LC_Curr == Invoice_Curr == BL_Curr]
  2. Expiry Check [Today <= Expiry_Date]
  3. Amount Check [Invoice_Total <= LC_Amount × (1 + Tol_Plus)]
  4. Quantity Check [BL_Qty <= LC_Qty × (1 + Tol_Plus)]
  5. Shipment Date [BL_OnBoardDate <= LC_LatestShipmentDate]
  6. Port Matching [semantic_match(ports)]
  7. Party Names [applicant in invoice_buyer, beneficiary in invoice_seller]

Output: List of Discrepancy objects (empty if all pass)

Each Discrepancy contains:
  - field: str (which field failed)
  - lc_requirement: str (what LC says)
  - actual_value: str (what we found)
  - severity: "Tier1" (blocks payment)
"""
```

**Tool 8: `validate_tier2_checks(lc_data, docs_dict) -> list[Issue]`**
```python
"""
Perform Tier 2 (important) validation checks

Checks:
  1. Document Completeness [all required docs present?]
  2. Special Conditions [are they satisfied?]
  3. Description Matching [semantic + ISBP 745 rules]
  4. Document Cross-References [invoice #, B/L # consistency]
  5. Certificate Presence [if CIF, insurance cert present?]
  6. Partial Shipment [if restricted, only 1 B/L?]
  7. Transhipment Check [if not allowed, no tranship notation?]

Output: List of Issue objects

Each Issue contains:
  - field: str
  - severity: "Tier2" (flag but may be resolved)
  - description: str (what failed)
  - mitigation: str (can applicant waive this?)
"""
```

**Tool 9: `generate_compliance_report(tier1_results, tier2_results, semantic_scores) -> dict`**
```python
"""
Generate final compliance verdict with reasoning

Output JSON:
{
  "final_verdict": "COMPLIANT | DISCREPANCY | MINOR_DISCREPANCY",
  "confidence_score": 0.95,  # 0-1
  "discrepancies": [
    {
      "field": "amount",
      "lc_requirement": "USD 500,000",
      "actual_value": "USD 520,000",
      "impact": "Tier1 (blocked)",
      "isbp_reference": null
    }
  ],
  "compliances": [
    {
      "field": "goods_description",
      "reason": "Invoice specific (iPhone 15 Pro Max) matches B/L generic (Electronic Devices) per ISBP 745 Art. E26",
      "similarity_score": 0.72
    }
  ],
  "isbp_notes": [
    "ISBP 745 Art. E26 allows generic descriptions on B/L when invoice provides specificity",
    "ISBP 745 Art. C6 permits port name abbreviations and country additions"
  ],
  "reasoning": "Although invoice amount exceeds LC by USD 20,000, this falls within the 10% plus tolerance per LC terms. All other Tier 1 checks passed. Semantic analysis confirms goods description hierarchy acceptable per ISBP 745. RECOMMENDATION: APPROVE with standard documentary review."
}
```

---

### Implementation Stack

**Language:** Python 3.10+

**Key Libraries:**
- `pypdf` or `pdfplumber` - PDF extraction
- `openai` - text-embedding-3-small API
- `langchain` - LLM chain orchestration
- `anthropic` - Claude API for NLP
- `pydantic` - Data validation
- `python-dateutil` - Date parsing

**Architecture:**
```
mcp_tools/
├── extractors.py
│   ├── extract_lc_requirements()
│   ├── extract_invoice_details()
│   ├── extract_bl_details()
│   └── extract_packing_list_details()
├── semantic_tools.py
│   ├── semantic_similarity()
│   └── apply_isbp745_rules()
├── validators.py
│   ├── validate_tier1_checks()
│   ├── validate_tier2_checks()
│   └── generate_compliance_report()
├── models.py
│   ├── LCData (pydantic model)
│   ├── InvoiceData (pydantic model)
│   ├── BLData (pydantic model)
│   ├── Discrepancy (pydantic model)
│   ├── ComplianceReport (pydantic model)
└── constants.py
    ├── ISBP745_RULES
    ├── UCP600_STANDARDS
    └── SIMILARITY_THRESHOLDS
```

---

## Phase 3: LangGraph Workflow ⏳ READY TO START

### LangGraph Agent Architecture

**Graph Structure:**
```
start
  ↓
parse_lc_node
  ↓
parse_invoice_node (parallel)
parse_bl_node (parallel)
parse_packing_list_node (parallel)
  ↓ (synchronize)
tier1_validation_node
  ↓
[DECISION] Did Tier 1 pass?
  ├─ NO → consolidate_verdict_node (DISCREPANCY)
  └─ YES ↓
semantic_matching_node
  ↓
isbp745_reasoning_node
  ↓
tier2_validation_node
  ↓
consolidate_verdict_node
  ↓
end
```

**Node Definitions:**

**1. parse_lc_node(state: AgentState)**
```python
def parse_lc_node(state):
    lc_path = state["documents"]["lc"]
    lc_data = extract_lc_requirements(lc_path)
    state["extracted"]["lc"] = lc_data
    return state
```

**2. parse_invoice_node(state: AgentState)**
```python
def parse_invoice_node(state):
    invoice_path = state["documents"]["invoice"]
    invoice_data = extract_invoice_details(invoice_path)
    state["extracted"]["invoice"] = invoice_data
    return state
```

**3. tier1_validation_node(state: AgentState)**
```python
def tier1_validation_node(state):
    lc = state["extracted"]["lc"]
    invoice = state["extracted"]["invoice"]
    bl = state["extracted"]["bl"]
    
    discrepancies = validate_tier1_checks(lc, invoice, bl)
    state["tier1_discrepancies"] = discrepancies
    state["tier1_passed"] = len(discrepancies) == 0
    
    return state

def tier1_decision(state):
    return "tier1_pass" if state["tier1_passed"] else "tier1_fail"
```

**4. semantic_matching_node(state: AgentState)**
```python
def semantic_matching_node(state):
    lc_desc = state["extracted"]["lc"]["goods_description"]
    invoice_desc = state["extracted"]["invoice"]["items"][0]["description"]
    bl_desc = state["extracted"]["bl"]["goods_description"]
    
    score_inv_lc = semantic_similarity(invoice_desc, lc_desc)
    score_bl_inv = semantic_similarity(bl_desc, invoice_desc)
    score_bl_lc = semantic_similarity(bl_desc, lc_desc)
    
    isbp_compliant = apply_isbp745_rules(lc_desc, invoice_desc, bl_desc)
    
    state["semantic_scores"] = {
        "invoice_vs_lc": score_inv_lc,
        "bl_vs_invoice": score_bl_inv,
        "bl_vs_lc": score_bl_lc,
        "isbp745_compliant": isbp_compliant
    }
    
    return state
```

**5. consolidate_verdict_node(state: AgentState)**
```python
def consolidate_verdict_node(state):
    report = generate_compliance_report(
        tier1_results=state["tier1_discrepancies"],
        tier2_results=state.get("tier2_issues", []),
        semantic_scores=state.get("semantic_scores", {})
    )
    
    state["compliance_report"] = report
    return state
```

**AgentState Definition:**
```python
from typing import TypedDict, Any

class AgentState(TypedDict):
    documents: dict  # {"lc": path, "invoice": path, "bl": path, "packing_list": path}
    extracted: dict  # {"lc": LCData, "invoice": InvoiceData, ...}
    tier1_discrepancies: list
    tier1_passed: bool
    tier2_issues: list
    semantic_scores: dict
    compliance_report: ComplianceReport
    error: str | None
```

---

## Phase 4: Integration Testing ⏳ READY TO START

### Test Plan

**Test Case 1: Apple iPhone Import (COMPLIANT)**
```python
def test_apple_import():
    files = {
        "lc": "mock_documents/1_APPLE_IPHONE_IMPORT/LC_LC-2026-001-HSBC.md",
        "invoice": "mock_documents/1_APPLE_IPHONE_IMPORT/INVOICE_INV-2026-00145.md",
        "bl": "mock_documents/1_APPLE_IPHONE_IMPORT/BL_MAEU123456789.md",
        "packing_list": "mock_documents/1_APPLE_IPHONE_IMPORT/PACKING_LIST_PL-2026-00145.md"
    }
    
    result = compliance_agent.invoke({"documents": files})
    
    assert result["compliance_report"]["final_verdict"] == "COMPLIANT"
    assert result["compliance_report"]["confidence_score"] > 0.90
    assert "ISBP 745 Art. E26" in result["compliance_report"]["reasoning"]
```

**Test Case 2: Vietnamese Textile (Special Conditions)**
```python
def test_textile_special_conditions():
    files = {...}  # Textile dataset
    
    # If pre-shipment inspection cert is MISSING:
    result = compliance_agent.invoke({"documents": files})
    
    assert "Pre-shipment inspection" in [issue["field"] for issue in result["tier2_issues"]]
```

**Test Case 3: Automotive Transhipment (Restrictions)**
```python
def test_automotive_transhipment():
    files = {...}  # Automotive dataset
    
    result = compliance_agent.invoke({"documents": files})
    
    # LC says transhipment NOT allowed
    # B/L shows no transhipment
    assert "transhipment" not in result["compliance_report"]["discrepancies"]
```

**Test Case 4: Amount Exceeds Tolerance (DISCREPANCY)**
```python
def test_amount_exceeds_tolerance():
    # Modified invoice: USD 600,000 (exceeds USD 550,000 max with 10% tolerance)
    result = compliance_agent.invoke({"documents": files})
    
    assert result["compliance_report"]["final_verdict"] == "DISCREPANCY"
    assert "amount" in [d["field"] for d in result["tier1_discrepancies"]]
```

---

## Phase 5: Production Deployment ⏳ FUTURE

### Deployment Architecture

```
User Interface (Streamlit)
    ↓
FastAPI Backend
    ↓
LangGraph Agent
    ↓
MCP Tools (Python)
    └─ Document Extractors
    └─ Semantic Matchers
    └─ Validators
    ↓
External APIs
    └─ OpenAI (embeddings, LLM)
    └─ Anthropic (Claude)
    ↓
Storage
    └─ Document Archive
    └─ Compliance Reports (PostgreSQL)
```

---

## Success Criteria

### Phase 1 ✅ ACHIEVED
- [x] PICK strategy documented (17.7 KB)
- [x] LC reference complete (24.2 KB)
- [x] 3 mock datasets created (12 files, 60+ KB)
- [x] All files in GitHub repo

### Phase 2 (MCP Tools) - Next
- [ ] 9 MCP tools implemented
- [ ] 100% docstring coverage
- [ ] Unit tests for each tool
- [ ] Integration tests with mock data
- [ ] Similarity threshold tuning (optimal: 0.70-0.85)

### Phase 3 (LangGraph) - Next
- [ ] Graph structure implemented
- [ ] 9 nodes defined and tested
- [ ] State management complete
- [ ] End-to-end workflow tested
- [ ] Error handling implemented

### Phase 4 (Integration) - Next
- [ ] All 3 mock datasets pass tests
- [ ] Compliance reports generated correctly
- [ ] ISBP 745 rules correctly applied
- [ ] Confidence scores validated
- [ ] Performance benchmarked

---

## Next Immediate Steps

### 1. Set Up MCP Tools Project
```bash
mkdir mcp_tools
cd mcp_tools
python -m venv venv
source venv/bin/activate
pip install pypdf pydantic openai anthropic python-dateutil
```

### 2. Start with Extractor Tools
```
# Priority order:
1. extract_lc_requirements() - Test with 1_APPLE_IPHONE_IMPORT
2. extract_invoice_details() - Test with same
3. extract_bl_details() - Test with same
4. extract_packing_list_details() - Test with same
```

### 3. Test Each Tool
```python
# Example test
from mcp_tools.extractors import extract_lc_requirements

lc_path = "mock_documents/1_APPLE_IPHONE_IMPORT/LC_LC-2026-001-HSBC.md"
lc_data = extract_lc_requirements(lc_path)

print(lc_data)
assert lc_data["lc_number"] == "LC/2026/001/HSBC"
assert lc_data["amount"] == 500000
assert lc_data["currency"] == "USD"
print("✅ Test passed")
```

### 4. Build LangGraph Graph
```
Once extractors working:
1. Define AgentState
2. Create node functions
3. Build graph with edges
4. Test state flow
```

### 5. Run Integration Tests
```
With working graph:
1. Test with Dataset 1 (Apple) - should be COMPLIANT
2. Test with Dataset 2 (Textile) - check special conditions
3. Test with Dataset 3 (Automotive) - check restrictions
4. Create modified versions for DISCREPANCY scenarios
```

---

## Key Insights & Learnings

### 1. Description Matching is Non-Trivial
```
Problem:
  "iPhone 15 Pro Max" != "Electronic Devices" (string level)
  But acceptable under ISBP 745
  
Solution:
  1. Use embeddings (semantic similarity)
  2. Apply ISBP 745 rules
  3. Check hierarchy (specific -> generic acceptable)
  4. Threshold: 0.70-0.85 (tunable)
```

### 2. Parties Matching Requires Fuzzy Logic
```
Problem:
  Invoice Buyer: "TechWorld Distribution Ltd"
  B/L Consignee: "TechWorld Dist Ltd"
  (exact match fails)
  
Solution:
  Use fuzzy string matching (difflib, fuzzywuzzy)
  Or semantic similarity for company names
  Threshold: 0.85+ for party matching
```

### 3. ISBP 745 is Critical to Compliance
```
Without ISBP 745:
  "Apple iPhone" describes very different from "Electronic Devices"
  System would flag as DISCREPANCY
  
With ISBP 745:
  Art. E26: "B/L descriptions may be general terms"
  System understands acceptable hierarchy
  Marks as COMPLIANT
  
Conclusion: ISBP 745 rules MUST be encoded explicitly
```

### 4. Tolerance Bands are Tolerance Bands
```
Common Mistake:
  If Invoice > LC Amount → DISCREPANCY
  
Correct Logic:
  Invoice must be <= LC Amount × (1 + Tolerance_Plus%)
  Dataset 1: 520,000 <= 550,000 ✓ (within 10% tolerance)
```

### 5. Partial vs Full Shipment
```
If LC allows "Partial shipments allowed (max 3)":
  System can accept multiple B/Ls (up to 3)
  Total Quantity across all B/Ls must still respect LC limits
  
If LC says no transhipment:
  B/L must show direct port-to-port
  No transhipment notation (no vessel changes)
```

---

## References & Standards

1. **UCP 600** - Uniform Customs and Practice for Documentary Credits
   - Art. 14: Examination of documents (5 banking days)
   - Standard of examination: reasonable care

2. **ISBP 745** - International Standard Banking Practice (latest)
   - Art. E26: B/L description may be general terms
   - Art. C6: Port names permit abbreviations and country additions
   - Crucial for description matching logic

3. **Incoterms 2020**
   - CIF (Cost, Insurance, Freight)
   - FOB (Free on Board)
   - Determines party responsibilities

4. **Trade Finance Standards**
   - ISO 9001: Quality Management System
   - Pre-shipment Inspection Guidelines
   - Certificate of Origin requirements

---

## Contact & Support

**Questions about PICK Strategy?** → See [docs/PICK_STRATEGY.md](../docs/PICK_STRATEGY.md)

**LC Reference Needed?** → See [docs/LC_TYPES_DETAILS_PARTIES.md](../docs/LC_TYPES_DETAILS_PARTIES.md)

**Mock Dataset Details?** → See [mock_documents/README.md](../mock_documents/README.md)

---

**Status:** Phase 1 Complete ✅

**Ready to proceed with Phase 2 (MCP Tools)?** 🚀 YES!

**Updated:** 2026-01-13, 19:30 HKT
