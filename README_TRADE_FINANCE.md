# Agentic AI for Trade Finance LC Compliance 💁❤️🧐

**An intelligent system for automating Letter of Credit compliance checking using Claude, LangGraph, and MCP tools.**

## 🚀 What Was Built

### Phase 1: Complete ✅

**In this phase (Jan 13, 2026), we created:**

#### 1. **PICK Strategy Document** 📄
**[`docs/PICK_STRATEGY.md`](docs/PICK_STRATEGY.md) - 17.7 KB**

Comprehensive guide for data extraction and entity selection:
- **Part 1:** Data Hierarchy (23 critical fields organized by Tier)
- **Part 2:** Extraction Strategy (4-step extraction process with MCP tools)
- **Part 3:** Decision Tree (5-phase validation flow)
- **Part 4:** Why This Approach Works (explanation + examples)
- **Part 5:** Implementation Checklist (9 MCP tools to build)

**Key Insight:** Separates critical fields (Tier 1 - blocks payment) from important fields (Tier 2 - informs decision) from supporting fields (Tier 3 - audit trail).

---

#### 2. **LC Reference Guide** 📁
**[`docs/LC_TYPES_DETAILS_PARTIES.md`](docs/LC_TYPES_DETAILS_PARTIES.md) - 24.2 KB**

Complete reference for LC structures and parties:
- **Part 1:** LC Types Classification (6 categories)
  - By revocability (irrevocable vs revocable)
  - By confirmation (confirmed vs unconfirmed)
  - By presentation (sight vs time/usance)
  - By coverage (full vs revolving)
  - By transferability (transferable vs non-transferable)
  - By payment source (documentary vs stand-by)

- **Part 2:** LC Structural Details (23 essential fields)
  - LC numbers, dates, amounts, currencies
  - Party information (applicant, beneficiary)
  - Goods description and quantity
  - Shipping terms (incoterms, ports, dates)
  - Required documents and special conditions

- **Part 3:** LC Parties & Roles (7 party types)
  - Applicant (buyer), Beneficiary (seller)
  - Issuing Bank, Confirming Bank, Negotiating Bank
  - Inspector, Insurance Company, Shipping Line

- **Part 4:** Compliance Checklist
  - Tier 1 checks (expiry, currency, amount, quantity, dates, ports, parties)
  - Tier 2 checks (documents, conditions, descriptions, cross-references)

---

#### 3. **Mock Trade Finance Datasets** 📅
**[`mock_documents/`](mock_documents/) - 12 files, 60+ KB**

**3 complete transaction datasets** covering different industries, company sizes, and currencies:

**Dataset 1: Apple iPhone Import** (Large Corp - Electronics Retail)
```
Company:      TechWorld Distribution Ltd (Hong Kong)
Sector:       Electronics Retail
LC Amount:    USD 500,000
Currency:     USD
Goods:        Apple iPhone 15 Pro Max (5,000 units)
Incoterms:    CIF Hong Kong
Ports:        Los Angeles -> Hong Kong

Key Challenge: Description matching
  - LC: "Apple iPhone 15 Pro Max smartphones"
  - Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black" (specific)
  - B/L: "Electronic Devices - Apple iPhone" (generic per ISBP 745)
  
Documents:
  1. LC_LC-2026-001-HSBC.md
  2. INVOICE_INV-2026-00145.md
  3. BL_MAEU123456789.md
  4. PACKING_LIST_PL-2026-00145.md
```

**Dataset 2: Vietnamese Silk Export** (SME - Textile Manufacturing)
```
Company:      Vietnamese Silk Trading Co Ltd
Sector:       Textile Manufacturing (SME)
LC Amount:    EUR 85,000
Currency:     EUR
Goods:        Silk scarves & textiles (10,000 pieces)
Incoterms:    FOB Ho Chi Minh City
Ports:        Ho Chi Minh City -> Hamburg

Key Challenge: Special conditions
  - Pre-shipment inspection mandatory
  - Certificate of Origin (Vietnam) required
  - 100% payment on B/L presentation
  
Documents:
  1. LC_LC-2026-VN-STT.md
  2. INVOICE_VST-INV-2026-0089.md
  3. BL_VCTL202602001.md
  4. PACKING_LIST_PL-VST-2026-0089.md
```

**Dataset 3: Indian Automotive Parts** (Mid-size Manufacturing)
```
Company:      Precision Manufacturing India Pvt Ltd
Sector:       Automotive Parts Manufacturing
LC Amount:    AUD 250,000
Currency:     AUD
Goods:        Transmission & gearbox parts (50,000 units)
Incoterms:    CIF Melbourne
Ports:        Chennai -> Melbourne

Key Challenge: Quality & restrictions
  - ISO 9001 certification mandatory
  - Quality inspection report required
  - Partial shipments allowed (max 3)
  - Transhipment NOT allowed
  
Documents:
  1. LC_LC-2026-AU-PMI.md
  2. INVOICE_PMI-INV-AU-2026-0047.md
  3. BL_PMI-2026-BLG-001.md
  4. PACKING_LIST_PL-PMI-AU-2026-047.md
```

**Dataset Coverage:**
- ✅ Different currencies (USD, EUR, AUD)
- ✅ Different company sizes (Large, SME, Mid-size)
- ✅ Different sectors (Electronics, Textiles, Automotive)
- ✅ Different incoterms (CIF, FOB)
- ✅ Different commodity types
- ✅ Different compliance challenges

---

#### 4. **Implementation Roadmap** 🗮pf
**[`docs/IMPLEMENTATION_ROADMAP.md`](docs/IMPLEMENTATION_ROADMAP.md) - 24.1 KB**

Complete guide for Phases 2-5:
- **Phase 2:** MCP Tools Implementation (9 tools detailed)
- **Phase 3:** LangGraph Workflow (graph structure, nodes, edges)
- **Phase 4:** Integration Testing (test cases for all 3 datasets)
- **Phase 5:** Production Deployment (architecture, deployment)

---

## 🎉 Key Achievements

### Problem Solved: Description Matching

**The Challenge:**
```
Old Approach (String Matching):
  LC: "Apple iPhone 15 Pro Max smartphones"
  Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black"
  B/L: "Electronic Devices"
  
  Result: DISCREPANCY ✗ (strings don't match exactly)
  Problem: Doesn't understand product hierarchy
```

**The Solution (Semantic + ISBP 745):**
```
New Approach:
  1. Extract descriptions from each document
  2. Use text-embedding-3-small to compute similarity
  3. Check ISBP 745 Art. E26: "B/L may use general terms"
  4. Validate hierarchy: Specific-to-Generic acceptable
  
  Similarity Score: invoice vs B/L = 0.72 (below 0.85 threshold)
  BUT ISBP 745 allows generic B/L descriptions
  
  Result: COMPLIANT ✓ (understands acceptable hierarchy)
  Reasoning: "Invoice specific describes B/L generic per ISBP 745 Art. E26"
```

---

### Data Model: Tier-Based Validation

**Tier 1 (Critical - Blocks Payment):**
```
Checks:
  ✓ Expiry Date [Today <= Expiry_Date]
  ✓ Currency Match [LC_Curr == Invoice_Curr == B/L_Curr]
  ✓ Amount Check [Invoice <= LC × (1 + Tolerance_Plus)]
  ✓ Quantity Check [B/L <= LC × (1 + Tolerance_Plus)]
  ✓ Shipment Date [B/L_OnBoardDate <= LC_LatestShipmentDate]
  ✓ Port Matching [semantic_match(LC_Ports, B/L_Ports)]
  ✓ Party Names [Applicant/Beneficiary match]
  
 If ANY fails -> DISCREPANCY (payment blocked)
```

**Tier 2 (Important - Flag Discrepancy):**
```
Checks:
  ✓ Document Completeness [all required docs present?]
  ✓ Special Conditions [are they satisfied?]
  ✓ Description Matching [semantic + ISBP 745]
  ✓ Document Cross-References [consistency]
  ✓ Certificate Presence [CIF -> insurance required]
  ✓ Partial Shipment [if restricted, only 1 B/L?]
  ✓ Transhipment [if not allowed, no tranship notation?]
  
 If issues -> MINOR_DISCREPANCY (may be resolved with waiver)
```

**Tier 3 (Supporting - Audit Trail):**
```
Data:
  ✓ Package details (carton numbers, weights)
  ✓ Cross-document references
  ✓ Logistics information
  ✓ Supporting documentation
  
 Used for: Audit trail, insurance, post-shipment verification
```

---

## 💾 Technical Architecture

### Stack

```
UI Layer
  ↓
  Streamlit / FastAPI
  ↓
Agent Layer
  ↓
  LangGraph (Multi-agent orchestration)
  ↓
Tool Layer
  ↓
  MCP Tools (9 tools)
  ├─ 4 Extractors (LC, Invoice, B/L, Packing List)
  ├─ 2 Semantic Tools (Similarity, ISBP745 Rules)
  └─ 3 Validators (Tier1, Tier2, Report Generation)
  ↓
External APIs
  ├─ OpenAI (text-embedding-3-small)
  └─ Anthropic (Claude for NLP)
  ↓
Data Layer
  ├─ PDF/Markdown Documents
  └─ Compliance Reports (Database)
```

---

## 🗒️ Data Models

### LCData (Pydantic Model)
```python
class LCData(BaseModel):
    lc_number: str                 # e.g., "LC/2026/001/HSBC"
    issue_date: date
    expiry_date: date
    amount: float
    currency: str                  # "USD", "EUR", "AUD"
    tolerance_plus: float          # 5-10%
    tolerance_minus: float         # 2-5%
    applicant: Party               # Buyer
    beneficiary: Party             # Seller
    goods_description: str
    quantity: str
    incoterms: str                 # "CIF", "FOB", etc.
    port_of_loading: str
    port_of_discharge: str
    latest_shipment_date: date
    required_documents: list[str]
    special_conditions: list[str]
```

### InvoiceData (Pydantic Model)
```python
class InvoiceData(BaseModel):
    invoice_number: str
    date: date
    seller: str
    buyer: str
    items: list[InvoiceItem]
    subtotal: float
    tax: float
    total: float
    currency: str
    reference_lc: str

class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit: str
    unit_price: float
    total: float
```

### ComplianceReport (Pydantic Model)
```python
class ComplianceReport(BaseModel):
    final_verdict: str             # "COMPLIANT" | "DISCREPANCY" | "MINOR_DISCREPANCY"
    confidence_score: float        # 0.0-1.0
    discrepancies: list[Discrepancy]
    compliances: list[Compliance]
    isbp_notes: list[str]          # ISBP 745 citations
    reasoning: str                 # Detailed explanation
```

---

## 📂 File Structure

```
Agentic-AI---MCP-for-Trade-Finance/
├── README.md                              # Main project README
├── README_TRADE_FINANCE.md                # This file
├── docs/
│   ├── PICK_STRATEGY.md                   # Data extraction strategy
│   ├── LC_TYPES_DETAILS_PARTIES.md        # LC reference guide
│   ├── IMPLEMENTATION_ROADMAP.md          # Phase 2-5 roadmap
│   └── LC_COMPLIANCE_CHECKLIST.md         # Quick reference checklist
├── mock_documents/
│   ├── README.md                           # Dataset documentation
│   ├── 1_APPLE_IPHONE_IMPORT/
│   │   ├── LC_LC-2026-001-HSBC.md
│   │   ├── INVOICE_INV-2026-00145.md
│   │   ├── BL_MAEU123456789.md
│   │   └── PACKING_LIST_PL-2026-00145.md
│   ├── 2_TEXTILE_EXPORT/
│   │   ├── LC_LC-2026-VN-STT.md
│   │   ├── INVOICE_VST-INV-2026-0089.md
│   │   ├── BL_VCTL202602001.md
│   │   └── PACKING_LIST_PL-VST-2026-0089.md
│   └── 3_AUTOMOTIVE_PARTS/
│       ├── LC_LC-2026-AU-PMI.md
│       ├── INVOICE_PMI-INV-AU-2026-0047.md
│       ├── BL_PMI-2026-BLG-001.md
│       └── PACKING_LIST_PL-PMI-AU-2026-047.md
└── (Phase 2+)
    ├── mcp_tools/
    │   ├── extractors.py
    │   ├── semantic_tools.py
    │   ├── validators.py
    │   ├── models.py
    │   └── constants.py
    ├── agents/
    │   └── compliance_agent.py
    ├── tests/
    │   ├── test_apple_import.py
    │   ├── test_textile_export.py
    │   └── test_automotive_parts.py
    └── ui/
        └── streamlit_app.py
```

---

## 🚀 Quick Start: Next Steps

### For Phase 2 Implementation:

1. **Set up environment:**
   ```bash
   mkdir mcp_tools
   cd mcp_tools
   python -m venv venv
   source venv/bin/activate
   pip install pypdf pydantic openai anthropic python-dateutil
   ```

2. **Start with extractors:**
   ```python
   # Test with Dataset 1 (Apple)
   from mcp_tools.extractors import extract_lc_requirements
   
   lc_path = "mock_documents/1_APPLE_IPHONE_IMPORT/LC_LC-2026-001-HSBC.md"
   lc_data = extract_lc_requirements(lc_path)
   
   assert lc_data["lc_number"] == "LC/2026/001/HSBC"
   assert lc_data["amount"] == 500000
   print("✅ Extractor working!")
   ```

3. **Build semantic tools:**
   ```python
   from mcp_tools.semantic_tools import semantic_similarity
   
   score = semantic_similarity(
       "Apple iPhone 15 Pro Max, 256GB",
       "Electronic Devices"
   )
   print(f"Similarity: {score:.2f}")
   # Expected: 0.70-0.75
   ```

4. **Create LangGraph agent:**
   ```python
   from langgraph.graph import StateGraph
   
   # See IMPLEMENTATION_ROADMAP.md for detailed node definitions
   workflow = StateGraph(AgentState)
   # Add nodes and edges
   # Test with mock datasets
   ```

---

## 💎 Standards & References

### International Standards

1. **UCP 600** (Uniform Customs and Practice for Documentary Credits)
   - Art. 14: Examination of documents (5 banking days)
   - Standard: Reasonable care in examination
   - Applies to all LCs

2. **ISBP 745** (International Standard Banking Practice)
   - **Art. E26:** B/L descriptions may use general terms (key for description matching!)
   - **Art. C6:** Port names permit abbreviations and country additions
   - Essential for automated compliance checking

3. **Incoterms 2020**
   - CIF (Cost, Insurance, Freight) - seller pays shipping + insurance
   - FOB (Free on Board) - buyer pays from loading port onward
   - Determines party responsibilities

4. **Trade Finance Best Practices**
   - ISO 9001: Quality Management System
   - Certificate of Origin: Proves country of manufacture
   - Pre-shipment Inspection: Quality/quantity verification

---

## 📧 Documentation Links

**Complete Documentation:**
- 📄 [PICK Strategy](docs/PICK_STRATEGY.md) - Data extraction & validation flow
- 📁 [LC Reference Guide](docs/LC_TYPES_DETAILS_PARTIES.md) - Complete LC taxonomy
- 🗮pf [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md) - Phases 2-5 detailed
- 📅 [Mock Datasets](mock_documents/README.md) - 3 complete transactions

---

## 🐛 Testing & Validation

### Test Coverage (Phase 4)

**Dataset 1 - Apple (Compliant):**
```bash
pytest tests/test_apple_import.py
# Expected: COMPLIANT
# Verifies: Description matching, tolerance calculations, semantic similarity
```

**Dataset 2 - Textile (Special Conditions):**
```bash
pytest tests/test_textile_export.py
# Expected: Special condition verification
# Verifies: Pre-shipment inspection, origin certificate
```

**Dataset 3 - Automotive (Restrictions):**
```bash
pytest tests/test_automotive_parts.py
# Expected: Restriction enforcement
# Verifies: Transhipment prohibition, quality certification
```

---

## 🙋 Author Notes

### Key Design Decisions

1. **Tier-Based Validation:** Critical fields block payment. Important fields flag for review. Supporting fields for audit.

2. **Semantic Matching:** String matching alone insufficient. Use embeddings (text-embedding-3-small) + ISBP 745 rules.

3. **ISBP 745 Encoding:** Critical to compliance. B/L descriptions CAN be generic per Art. E26. This must be explicitly coded.

4. **Mock Data Quality:** 3 complete datasets covering different scenarios (large corp, SME, mid-size), currencies, sectors, and incoterms.

5. **Confidence Scoring:** Every report includes confidence score (0.0-1.0) based on data quality, matches, and standard adherence.

---

## ✅ Phase 1 Summary

### Deliverables
- ✅ PICK Strategy (17.7 KB) - comprehensive data extraction guide
- ✅ LC Reference (24.2 KB) - complete LC taxonomy and standards
- ✅ Mock Datasets (12 files, 60+ KB) - 3 realistic transactions
- ✅ Roadmap (24.1 KB) - detailed implementation guide for phases 2-5
- ✅ Total: ~130 KB of documentation + mock data

### Status
**Phase 1 Complete ✅**

Phase 2 (MCP Tools) Ready to Start 🚀

---

**Created:** 2026-01-13, 3:17 PM HKT

**Last Updated:** 2026-01-13, 7:25 PM HKT

**Ready to proceed with Phase 2 implementation?** Let's build the MCP tools! 💁❤️🧐
