# PICK Strategy for Agentic AI Trade Finance System

## Overview

The **PICK** phase refers to the data extraction and entity selection strategy - determining **what data to extract** and **how to prioritize** it for the Reviewer Agent to make compliance decisions.

Given the complexity of trade finance documents, this document outlines:
1. **What to Pick:** Critical vs Secondary data fields
2. **How to Pick:** MCP tools and extraction priorities
3. **When to Pick:** Decision tree for multi-step extraction
4. **Why This Approach:** NLP reasoning + semantic matching for ISBP 745 compliance

---

## Part 1: What to PICK (Data Hierarchy)

### Tier 1: CRITICAL (Must Extract, Blocks Decision)
These fields directly impact compliance decisions. Missing or incorrect data = **STOP**.

| Field | Source | Why Critical | Validation Rule |
|-------|--------|--------------|------------------|
| **LC Amount** | LC Document | Cannot exceed this in Invoice | `Invoice_Total ≤ LC_Amount × (1 + Tolerance_Plus%)` |
| **LC Quantity** | LC Document | Cannot exceed this in shipment | `B/L_Quantity ≤ LC_Quantity × (1 + Tolerance_Plus%)` |
| **Goods Description (LC)** | LC Document 46A/C | Baseline for description matching | `Semantic_Similarity(Invoice_Desc, B/L_Desc) ≥ Threshold` |
| **Currency** | LC, Invoice, B/L | Must match across all docs | `LC_Currency == Invoice_Currency == B/L_Currency` |
| **Expiry Date** | LC Document | Presentation deadline | `Today ≤ Expiry_Date` |
| **Shipment Date** | LC, B/L | Goods must ship on time | `B/L_OnBoardDate ≤ LC_LatestShipmentDate` |
| **Port of Loading** | LC, B/L | Route verification | `Semantic_Match(LC_Port, B/L_Port)` (allows abbreviations) |
| **Port of Discharge** | LC, B/L | Delivery location | `Exact_Match_or_Semantic(LC_Port, B/L_Port)` |
| **Applicant Name** | Invoice, B/L | Buyer identification | `Applicant_Name in Invoice_Buyer_Name` (fuzzy match) |
| **Beneficiary Name** | Invoice, B/L | Seller identification | `Beneficiary_Name in Invoice_Seller_Name` (fuzzy match) |

### Tier 2: IMPORTANT (Extract, Informs Decision)
These fields provide context and can trigger deeper inspection.

| Field | Source | Purpose | Action if Missing |
|-------|--------|---------|--------------------|
| **Special Conditions** | LC Section 47 | Compliance prerequisites | Log as "Requires Verification" |
| **Required Documents** | LC Section 46 | Document checklist | Cross-check all submitted docs |
| **Insurance Requirements** | LC | Coverage validation | Verify insurance cert if required |
| **Certificate of Origin** | LC, Doc | Country of manufacture | Validate if specified in LC |
| **Tolerance Bands** | LC | Allow variance | Calculate max/min accepted amounts |
| **Partial Shipment Clause** | LC | Multiple deliveries allowed? | Flag if multiple B/Ls submitted |
| **Transhipment Clause** | LC | Intermediate vessel allowed? | Check B/L transhipment notation |

### Tier 3: SUPPORTING (Extract, Provides Audit Trail)
These fields support audit, insurance, and post-shipment verification.

| Field | Source | Purpose |
|-------|--------|----------|
| **Invoice Number** | Invoice | Cross-reference |
| **B/L Number** | B/L | Shipment tracking |
| **Vessel Name & Voyage** | B/L | Shipping confirmation |
| **Marks & Numbers** | B/L, Packing List | Package identification |
| **Weight & Dimensions** | Packing List | Logistics validation |
| **Freight Charges** | B/L | Cost accountability |

---

## Part 2: How to PICK (Extraction Strategy)

### Step 1: Extract from LC (Baseline Requirements)

**MCP Tool: `extract_lc_requirements(lc_pdf)`**

```python
function extract_lc_requirements(lc_pdf) -> dict:
    """
    Extract LC requirements as baseline for compliance.
    
    Returns:
    {
        'lc_number': str,
        'amount': float,
        'currency': str,
        'tolerance_plus': float,
        'tolerance_minus': float,
        'goods_description': str,  # Field 46C
        'quantity': str,
        'latest_shipment_date': date,
        'expiry_date': date,
        'port_of_loading': str,
        'port_of_discharge': str,
        'applicant': {'name': str, 'address': str},
        'beneficiary': {'name': str, 'address': str},
        'special_conditions': list[str],
        'required_documents': list[str]
    }
    """
```

**Extraction Priorities:**
1. ✅ Amounts & Currency (Tier 1 - Non-negotiable)
2. ✅ Dates & Ports (Tier 1 - Critical path items)
3. ✅ Parties identification (Tier 1 - KYC requirement)
4. ✅ Goods description & quantity (Tier 1 - Core matching)
5. ✅ Special conditions (Tier 2 - Might require additional verification)

---

### Step 2: Extract from Commercial Invoice (Amount & Description Verification)

**MCP Tool: `extract_invoice_details(invoice_pdf)`**

```python
function extract_invoice_details(invoice_pdf) -> dict:
    """
    Extract invoice details for amount and description matching.
    
    Returns:
    {
        'invoice_number': str,
        'invoice_date': date,
        'seller_name': str,
        'buyer_name': str,
        'total_amount': float,
        'currency': str,
        'items': [
            {
                'description': str,  # SPECIFIC (detail allowed)
                'quantity': float,
                'unit_price': float,
                'total': float
            }
        ],
        'original_lc_number': str  # From invoice body
    }
    """
```

**Extraction Priorities:**
1. ✅ Total amount & currency (Tier 1 - Amount check)
2. ✅ Item descriptions (Tier 1 - Compare with B/L)
3. ✅ Buyer/Seller names (Tier 1 - Party matching)
4. ✅ Quantity per item (Tier 1 - Quantity check)
5. ✅ Item count (Tier 2 - Completeness check)

**Key Logic:**
- Invoice description MUST be specific (Art. 18 UCP 600)
- May exceed detail in LC (e.g., "iPhone 15 Pro Max 256GB" vs "iPhone 15 Pro Max")
- Invoice amount MUST NOT exceed LC amount (after tolerance)

---

### Step 3: Extract from Bill of Lading (Port, Date, Goods Verification)

**MCP Tool: `extract_bl_details(bl_pdf)`**

```python
function extract_bl_details(bl_pdf) -> dict:
    """
    Extract B/L details for shipment and description matching.
    
    Returns:
    {
        'bl_number': str,
        'on_board_date': date,  # CRITICAL: Proof of shipment
        'shipper_name': str,
        'consignee_name': str,
        'notify_party': str,
        'port_of_loading': str,
        'port_of_discharge': str,
        'vessel_name': str,
        'voyage_number': str,
        'goods_description': str,  # GENERAL TERMS ALLOWED (ISBP 745 Art. E26)
        'quantity': str,
        'marks_numbers': str,
        'gross_weight': float,
        'net_weight': float,
        'number_of_packages': int,
        'freight_charges': str,
        'freight_payment': str
    }
    """
```

**Extraction Priorities:**
1. ✅ On-board date (Tier 1 - Proof of loading)
2. ✅ Port of loading & discharge (Tier 1 - Route verification)
3. ✅ Goods description (Tier 1 - Description matching, **but allows generic terms per ISBP 745**)
4. ✅ Quantity (Tier 1 - Undershipping check)
5. ✅ Shipper/Consignee names (Tier 1 - Party verification)
6. ✅ Vessel & voyage (Tier 2 - Shipping confirmation)

**Key Logic:**
- B/L description CAN be generic (e.g., "Electronic Devices" for "iPhone 15 Pro Max") - **ISBP 745 Art. E26**
- On-board date MUST be ≤ Latest Shipment Date in LC
- Quantity on B/L MUST NOT exceed LC quantity (undershipping is allowed)
- Port names allow abbreviations and country additions (ISBP 745 Art. C6)

---

### Step 4: Extract from Packing List (Package Details & Audit Trail)

**MCP Tool: `extract_packing_list_details(packing_list_pdf)`**

```python
function extract_packing_list_details(packing_list_pdf) -> dict:
    """
    Extract packing list for logistics and audit verification.
    
    Returns:
    {
        'packing_list_number': str,
        'date': date,
        'invoice_number': str,  # Cross-reference
        'bl_number': str,  # Cross-reference
        'total_cartons': int,
        'items': [
            {
                'carton_number': int,
                'description': str,
                'quantity': int,
                'net_weight': float,
                'gross_weight': float,
                'dimensions': str
            }
        ],
        'total_net_weight': float,
        'total_gross_weight': float
    }
    """
```

**Extraction Priorities:**
1. ✅ Total cartons & weights (Tier 2 - Cross-check with B/L)
2. ✅ Item descriptions (Tier 2 - Reconcile with Invoice & B/L)
3. ✅ Cross-references (Invoice #, B/L #) (Tier 3 - Audit trail)

---

## Part 3: When to PICK (Decision Tree)

### Phase 1: Immediate Extraction (Parallel)
Start with these immediately when documents received:

```
Received: [LC, Invoice, B/L, Packing List]
   ↓
   ├─→ extract_lc_requirements() [PARALLEL]
   ├─→ extract_invoice_details() [PARALLEL]
   ├─→ extract_bl_details() [PARALLEL]
   └─→ extract_packing_list_details() [PARALLEL]
   ↓
   Wait for all 4 extractions to complete
   ↓
   Proceed to Phase 2
```

### Phase 2: Tier 1 Validation (Sequential)
Check critical fields immediately; stop on failure:

```
Tier 1 Checks (Must Pass):
   ↓
   1. Currency Match? [LC_Curr == Invoice_Curr == B/L_Curr]
      NO → DISCREPANCY: "Currency Mismatch"
      YES → Continue
   ↓
   2. Expiry Check? [Today ≤ Expiry_Date]
      NO → DISCREPANCY: "LC Expired"
      YES → Continue
   ↓
   3. Amount Check? [Invoice_Total ≤ LC_Amount × (1 + Tol_Plus)]
      NO → DISCREPANCY: "Amount Exceeds LC"
      YES → Continue
   ↓
   4. Quantity Check? [B/L_Qty ≤ LC_Qty × (1 + Tol_Plus)]
      NO → DISCREPANCY: "Quantity Exceeds LC"
      YES → Continue
   ↓
   5. Shipment Date Check? [B/L_OnBoardDate ≤ LC_LatestShipmentDate]
      NO → DISCREPANCY: "Late Shipment"
      YES → Continue
   ↓
   6. Port Matching? [Semantic_Match(LC_Ports, B/L_Ports)]
      NO → DISCREPANCY: "Port Mismatch"
      YES → Continue
   ↓
   7. Party Matching? [Applicant Match + Beneficiary Match]
      NO → DISCREPANCY: "Party Name Mismatch"
      YES → Continue
   ↓
   All Tier 1 Checks PASSED → Proceed to Phase 3
```

### Phase 3: Tier 1+ Semantic Matching (NLP Phase)
Use embeddings for description matching:

```
Description Matching (CORE LOGIC):
   ↓
   Extract:
   - LC_Description (baseline)
   - Invoice_Description (specific, detailed)
   - B/L_Description (can be generic)
   ↓
   Use text-embedding-3-small to compute:
   - similarity(Invoice_Desc, LC_Desc) → Score A
   - similarity(B/L_Desc, Invoice_Desc) → Score B
   - similarity(B/L_Desc, LC_Desc) → Score C
   ↓
   Decision Logic:
   IF Score A ≥ 0.85 AND Score B ≥ 0.70
       → COMPLIANT: "Description hierarchy acceptable"
   ELIF Score C ≥ 0.80 AND ISBP745_Rule_Applies(B/L_Desc)
       → COMPLIANT: "B/L uses generic terms per ISBP 745 Art. E26"
   ELSE
       → DISCREPANCY: "Description mismatch - semantic similarity below threshold"
   ↓
   Also Check: Special_Conditions in LC
   IF "Product must be [Specific Origin/Type]"
       → Verify invoice/B/L match specific requirement
   ↓
   Proceed to Phase 4
```

### Phase 4: Tier 2 Validation (Contextual)
If Tier 1 + semantic passed, verify supporting documents:

```
Tier 2 Checks (Dependent on LC):
   ↓
   IF Special_Conditions_Exist:
       1. Certificate of Origin Present?
       2. Insurance Certificate Present? (if CIF terms)
       3. Pre-shipment Inspection Cert? (if required)
       4. Country of Origin Matches? (if specified)
   ↓
   IF Partial_Shipment_Allowed:
       → Multiple B/Ls OK (verify total ≤ LC)
   ELSE:
       → Only 1 B/L allowed
   ↓
   IF Transhipment_NOT_Allowed:
       → Check B/L for "Transhipment" notation
       → If found → DISCREPANCY
   ↓
   Cross-check Document References:
       - Invoice # mentioned in B/L?
       - B/L # mentioned in Packing List?
       - Consistency in dates?
   ↓
   Proceed to Phase 5
```

### Phase 5: Consolidate & Report
Final decision with ISBP 745 reasoning:

```
Consolidate Results:
   ↓
   IF No Discrepancies Found:
       → VERDICT: "COMPLIANT"
       → Reason: "All documents conform to LC requirements per UCP 600"
   ELSE IF Only Tier 2 Issues:
       → VERDICT: "MINOR DISCREPANCY"
       → Reason: "[List discrepancies], but ISBP 745 may permit resolution"
   ELSE IF Tier 1 Issues:
       → VERDICT: "DISCREPANCY"
       → Reason: "[List critical issues], approval contingent on issuer waiver"
   ↓
   Output JSON Report:
   {
     "final_verdict": "COMPLIANT|DISCREPANCY|MINOR_DISCREPANCY",
     "discrepancies": [{"field": str, "lc_requirement": str, "actual_value": str, "impact": "Tier1|Tier2"}],
     "compliances": [{"field": str, "reason": str}],
     "isbp_notes": ["ISBP 745 Art. E26 allows generic description on B/L", ...],
     "confidence_score": 0.0-1.0,
     "reasoning": str
   }
```

---

## Part 4: Why This PICK Strategy Works

### Problem: Trade Ops Document Checking is Non-Linear

**The Human Review Process:**
```
Trade Officer receives: [LC, Invoice, B/L, Packing List]
  ↓
  [Glances at amounts] "Does invoice exceed LC? No." → OK
  ↓
  [Checks dates] "Is shipment on time? Yes." → OK
  ↓
  [Reads description] "Invoice says iPhone, B/L says Electronic Device.
                       But is that OK per ISBP 745? Let me think...
                       Yes, B/L can be generic." → OK
  ↓
  [Checks special conditions] "Needs Tanzania origin? Yes, invoice states it." → OK
  ↓
  Decision: APPROVE ✓
  Reasoning: "Though wordings differ, they refer to same product. ISBP 745 permits this."
```

**Why Flat OCR Fails:**
```
OCR Output:
  Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black"
  B/L:     "Electronic Devices"
  ↓
  String Match: "iPhone" != "Electronic Devices"
  ↓
  Result: DISCREPANCY ✗
  Problem: No semantic understanding of hierarchy
```

**Why Our PICK Strategy Works:**
```
Step 1: Extract structured data (amounts, dates, parties)
        → Catch obvious errors (amount exceeds LC)
        ↓
Step 2: Tier 1 validation (math checks, date checks)
        → All hard constraints pass ✓
        ↓
Step 3: Semantic matching (embeddings)
        - similarity("iPhone", "Electronic Devices") ≈ 0.72
        - This is below 0.85 threshold BUT
        - ISBP 745 Art. E26 explicitly allows generic B/L descriptions
        ↓
Step 4: Apply ISBP 745 rules
        - "B/L can be general terms"
        - "Invoice is specific"
        - "This hierarchy is acceptable"
        ↓
Step 5: Reasoning: "Although descriptions differ in specificity, both refer to 
        the same product category. Per ISBP 745 Article E26, Bill of Lading 
        descriptions may use general terms when the Commercial Invoice provides 
        sufficient specificity. COMPLIANT."
```

### Key Advantages

1. **Hierarchical Matching:** Doesn't require exact string match; understands that "iPhone" ⊂ "Electronic Devices"
2. **Standards-Aware:** Applies UCP 600 & ISBP 745 automatically
3. **Explainable:** Agent provides reasoning ("per ISBP 745 Art. E26...")
4. **Extensible:** Easy to add new rules for different document types or commodities
5. **Scalable:** Parallel extraction + sequential validation avoids bottlenecks

---

## Part 5: Implementation Checklist

### MCP Tools to Build (Priority Order)

- [ ] **Priority 1: Core Extraction Tools**
  - [ ] `extract_lc_requirements(lc_pdf)` - LC parser
  - [ ] `extract_invoice_details(invoice_pdf)` - Invoice parser
  - [ ] `extract_bl_details(bl_pdf)` - B/L parser
  - [ ] `extract_packing_list_details(packing_list_pdf)` - Packing List parser

- [ ] **Priority 2: Semantic Matching Tools**
  - [ ] `semantic_similarity(text1: str, text2: str) -> float` - Embedding-based matching
  - [ ] `apply_isbp745_rules(lc_desc, invoice_desc, bl_desc) -> bool` - ISBP 745 logic

- [ ] **Priority 3: Validation Tools**
  - [ ] `validate_tier1_checks(lc_data, invoice_data, bl_data) -> list[Discrepancy]`
  - [ ] `validate_tier2_checks(lc_data, docs_dict) -> list[Issue]`
  - [ ] `generate_compliance_report(all_results) -> dict` - Final output

### LangGraph Nodes

```python
Nodes:
  1. parse_lc_node(state) → extracts LC requirements
  2. parse_invoice_node(state) → extracts invoice details
  3. parse_bl_node(state) → extracts B/L details
  4. parse_packing_list_node(state) → extracts packing list
  5. tier1_validation_node(state) → runs Tier 1 checks
  6. semantic_matching_node(state) → runs embeddings on descriptions
  7. isbp745_reasoning_node(state) → applies ISBP 745 rules
  8. tier2_validation_node(state) → checks special conditions
  9. consolidate_verdict_node(state) → generates final report
  
Edges (with conditional branching):
  parse_lc → [parse_invoice, parse_bl, parse_packing_list] (parallel)
  [parse_invoice, parse_bl, parse_packing_list] → tier1_validation_node (synchronize)
  tier1_validation_node → (if tier1_pass) semantic_matching_node else consolidate_verdict (DISCREPANCY)
  semantic_matching_node → isbp745_reasoning_node
  isbp745_reasoning_node → tier2_validation_node
  tier2_validation_node → consolidate_verdict_node
```

---

## Next Steps

1. **Build extraction tools** (OCR + NLP for PDF parsing)
2. **Implement semantic matching** with text-embedding-3-small
3. **Code ISBP 745 rules** as decision logic
4. **Create LangGraph workflow** with nodes and edges
5. **Test on 3 mock datasets** (already in `/mock_documents/`)
6. **Iterate on ISBP 745 threshold tuning** (what similarity score is "acceptable"?)

---

**Ready to build the agents? 🚀**
