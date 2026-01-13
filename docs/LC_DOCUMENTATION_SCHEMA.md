# Letter of Credit (LC) Documentation Schema

## Part 1: LC Types & Classification

### By Nature of Commitment
| Type | Definition | Key Feature |
|------|-----------|------------|
| **Revocable LC** | Can be cancelled/modified by issuer without beneficiary's consent | Rarely used; offers no security to beneficiary |
| **Irrevocable LC** | Cannot be cancelled without all parties' consent | Standard in international trade; provides security |
| **Confirmed LC** | Advising bank adds its own payment undertaking | Highest security; beneficiary has two payment sources |
| **Unconfirmed LC** | Only issuing bank is obligated to pay | Lower security than confirmed |

### By Method of Settlement
| Type | Settlement Mechanism | Typical Use |
|------|---------------------|------------|
| **Sight LC** | Payment made immediately upon document presentation | General merchandise |
| **Usance/Time LC** | Payment made at future date (e.g., 30/60/90 days after sight) | Higher-value goods; gives buyer credit period |
| **Deferred Payment LC** | Bank defers payment; does not accept drafts | Buyer gets extended credit |
| **Acceptance LC** | Buyer's bank accepts time draft drawn by beneficiary | Financing mechanism for buyer |
| **Negotiation LC** | Any bank can negotiate (purchase) compliant documents | Maximum flexibility for beneficiary |

### By Coverage & Special Features
| Type | Feature | Use Case |
|------|---------|----------|
| **Back-to-Back LC** | Importer's bank opens LC with exporter's bank using first LC as security | Trading houses; commodity merchants |
| **Transferable LC** | Beneficiary can transfer rights to another party | Intermediaries in supply chain |
| **Standby LC** | Secondary payment guarantee; used if primary obligation fails | Performance guarantees; bonds |
| **Red Clause LC** | Issuing bank provides pre-shipment advance to beneficiary | Financing for exporter's production |
| **Green Clause LC** | Covers warehouse/storage costs before shipment | Perishables; goods requiring storage |

---

## Part 2: LC Core Details (Fields as per UCP 600)

### 1. Identification & Parties (Art. 2, 10)

```json
{
  "lc_identification": {
    "lc_number": "string (e.g., 'LC/2024/001234')",
    "lc_date": "date",
    "issuing_bank_name": "string",
    "issuing_bank_swift": "string (BIC code)",
    "advising_bank_name": "string (if any)",
    "confirming_bank_name": "string (if LC is confirmed)"
  },
  "parties": {
    "applicant": {
      "party_type": "Buyer/Importer",
      "name": "string",
      "address": "string",
      "country": "string",
      "contact": "email/phone"
    },
    "beneficiary": {
      "party_type": "Seller/Exporter",
      "name": "string",
      "address": "string",
      "country": "string",
      "contact": "email/phone"
    }
  }
}
```

### 2. Credit Amount & Currency (Art. 2, 16)

```json
{
  "credit_amount": {
    "amount": "decimal",
    "currency": "string (ISO 4217, e.g., 'USD', 'EUR')",
    "amount_tolerance_plus": "percentage (e.g., 10%)",
    "amount_tolerance_minus": "percentage (e.g., 0%)",
    "total_maximum_amount": "decimal (after tolerance)",
    "cumulative": "boolean (can LC be used multiple times?)"
  }
}
```

### 3. Goods Description (Art. 18)

```json
{
  "goods_details": {
    "description": "string (must match Invoice & B/L; general terms allowed in B/L)",
    "hs_code": "string (Harmonized System code)",
    "quantity": "number + unit (e.g., '1000 units')",
    "unit_price": "decimal",
    "incoterms": "string (e.g., 'CIF Shanghai', 'FOB New York')"
  }
}
```

### 4. Shipment & Delivery Terms (Art. 3, 4)

```json
{
  "shipment_terms": {
    "port_of_loading": "string",
    "port_of_discharge": "string",
    "latest_shipment_date": "date",
    "date_of_expiry": "date (last day documents can be presented)",
    "place_of_expiry": "string (where documents must be presented)",
    "on_deck": "boolean (goods can be shipped on deck?)",
    "partial_shipment": "boolean (allowed?)",
    "transhipment": "boolean (allowed?)"
  }
}
```

### 5. Required Documents (Art. 6)

```json
{
  "required_documents": [
    {
      "document_type": "string (e.g., 'Commercial Invoice', 'Bill of Lading')",
      "quantity": "number of copies",
      "specifications": "object"
    }
  ],
  "example_doc_list": [
    {
      "document_type": "Commercial Invoice",
      "copies": 3,
      "signed_by": "Beneficiary",
      "must_show": ["Applicant as buyer", "Description matching LC", "Amount not exceeding LC"]
    },
    {
      "document_type": "Bill of Lading (Ocean)",
      "copies": 3,
      "signed_by": "Carrier/Agent",
      "must_show": ["Port of loading", "Port of discharge", "On board date", "Goods description (can be general)"]
    },
    {
      "document_type": "Packing List",
      "copies": 2,
      "signed_by": "Exporter",
      "must_show": ["Item details", "Weight/dimensions per package", "Total packages"]
    },
    {
      "document_type": "Certificate of Origin",
      "copies": 1,
      "signed_by": "Chamber of Commerce",
      "must_show": ["Goods origin country", "Beneficiary signature"]
    }
  ]
}
```

### 6. Additional Terms & Conditions (Art. 7)

```json
{
  "special_conditions": {
    "insurance_required": "boolean",
    "insurance_coverage": "string (e.g., '110% of invoice value')",
    "inspection_required": "boolean (Pre-shipment Inspection?)",
    "inspection_agency": "string (e.g., 'SGS', 'Bureau Veritas')",
    "inspection_certificate_needed": "boolean",
    "additional_notes": "string (e.g., 'Goods must be New Zealand origin', 'Max order qty 500 units per consignment')"
  }
}
```

---

## Part 3: Parties Involved

### Primary Parties

| Party | Role | Responsibility |
|-------|------|-----------------|
| **Applicant (Buyer/Importer)** | Requests LC from their bank | Pays bank for LC; accepts goods; indemnifies bank for any loss |
| **Beneficiary (Seller/Exporter)** | Receives payment upon document compliance | Ships goods; prepares required documents; presents documents to bank |
| **Issuing Bank** | Issues LC on behalf of applicant | Primary payment obligation; examines documents; decides on compliance |
| **Advising Bank** | Advises beneficiary of LC existence/terms | Forwards LC; may examine documents; may add confirmation |
| **Confirming Bank** | Adds own payment undertaking (if LC is confirmed) | Second payment source; reduces beneficiary's bank risk |
| **Negotiating Bank** | Purchases (negotiates) compliant documents from beneficiary | Acts as intermediary; typically paid by issuing bank |

### Secondary Parties

| Party | Role |
|-------|------|
| **Carrier/Shipping Line** | Issues Bill of Lading; transports goods |
| **Freight Forwarder** | Arranges shipping; prepares documentation |
| **Insurance Company** | Issues insurance certificate if required |
| **Inspector/Surveyor** | Conducts pre-shipment inspection if required |
| **Customs Authority** | Clears goods; issues certificate of origin |

---

## Part 4: Document Flow (UCP 600 Art. 14)

### Compliance Examination Standard

Banks examine documents **on their face alone** (Article 14(a)):
- **Literal Compliance:** Documents must match LC requirements literally, BUT
- **ISBP 745 (International Standard Banking Practice):** Allows reasonable interpretation
  - **Example 1:** LC says "Port of Loading: Shanghai", B/L says "Port: Shanghai, China" → **COMPLIANT** (ISBP 745 Art. C6)
  - **Example 2:** Invoice says "iPhone 15", B/L says "Electronic Devices" → **COMPLIANT** (ISBP 745 Art. C3: B/L descriptions can be general)
  - **Example 3:** Invoice quantity 100 units, B/L quantity 101 units → **DISCREPANCY** (Art. 18: quantities must not exceed LC)

### Document Hierarchy for Description Matching

| Document | Description Rule |
|----------|-----------------|
| **Commercial Invoice** | Must match LC **exactly** (Art. 18); specific; itemized |
| **Bill of Lading** | Can be **general terms** (ISBP 745 Art. E26); e.g., "Consumer Electronics" for "iPhone" |
| **Packing List** | Details for customs/logistics; doesn't need to match LC word-for-word |
| **Certificate of Origin** | Must show country matching LC requirements |

---

## Part 5: Common Discrepancies & How Agents Should Handle Them

### Category A: Discrepancies (Requires Amendment or Waiver)
```
Scenario 1: Amount Mismatch
- LC: USD 100,000
- Invoice: USD 105,000
- Status: DISCREPANCY (exceeds LC amount per Art. 18)
- Agent Logic: "Quantity increased, so amount increased. This is NOT compliant per UCP 600."

Scenario 2: Quantity Mismatch
- LC: 1,000 units
- B/L: 999 units
- Status: COMPLIANT (Art. 18 allows less than LC quantity)
- Agent Logic: "Undershipping is allowed."

Scenario 3: Port Mismatch (Literal)
- LC: "Port of Loading: Shanghai"
- B/L: "Shanghai, PRC"
- Status: COMPLIANT (ISBP 745 allows additional country reference)
- Agent Logic: "Identifies same port; ISBP 745 permits country addition."
```

### Category B: Description Mismatches (Handled by ISBP 745)
```
Scenario 4: Generic vs. Specific Description
- LC: "Electronic Goods, specifically Apple Products"
- Invoice: "iPhone 15 Pro Max, 256GB, Silver"
- B/L: "Electronic Goods"
- Status: COMPLIANT (Invoice specific, B/L general; both acceptable per ISBP 745)
- Agent Logic: "Invoice provides specificity; B/L uses general terms per ISBP 745 Art. E26."

Scenario 5: Partial Brand/Model Reference
- LC: "Smartphones"
- Invoice: "iPhone 15"
- B/L: "Mobile Devices"
- Status: COMPLIANT (Hierarchical specificity)
- Agent Logic: "All refer to same product category; descriptions are consistent in spirit."
```

### Category C: Document Structural Issues
```
Scenario 6: Missing Signature
- Document: Invoice without beneficiary signature
- LC Requirement: "Beneficiary signature required"
- Status: DISCREPANCY
- Agent Logic: "Signature is mandatory per document requirement; missing = non-compliant."

Scenario 7: Unsigned B/L
- LC Requirement: "B/L must be signed"
- Actual B/L: Computer-generated, no signature
- Status: Generally COMPLIANT in modern trade (computer-generated acceptable)
- Agent Logic: "Modern B/L practice allows unsigned; check if LC explicitly requires signature."
```

---

## Part 6: MCP Integration Points

For your Agentic AI system, these are the **MCP tools** you'll need:

### Tool 1: `extract_lc_details(lc_pdf)`
**Input:** Raw LC PDF  
**Output:** Structured LC JSON (all fields from Part 2)  
**Implementation:** OCR + NLP to parse standard LC forms

### Tool 2: `extract_invoice_details(invoice_pdf)`
**Input:** Commercial Invoice PDF  
**Output:** Structured JSON with description, amount, quantity, currency  

### Tool 3: `extract_bl_details(bl_pdf)`
**Input:** Bill of Lading PDF  
**Output:** Structured JSON with port, goods description, on-board date, quantity  

### Tool 4: `extract_packing_list_details(packing_list_pdf)`
**Input:** Packing List PDF  
**Output:** Structured JSON with packages, weights, descriptions  

### Tool 5: `check_compliance(lc_data, invoice_data, bl_data, packing_list_data)`
**Input:** Structured data from all four documents  
**Output:** JSON with compliance status, discrepancies list, ISBP 745 reasoning  
**Logic:** Implements the discrepancy rules from Part 5

---

## Part 7: Your "Pick" Strategy for POC

### Recommended Approach: **ReAct Pattern with LangGraph**

**Nodes in Graph:**
1. **Node 1: Parse LC** → Extract LC requirements
2. **Node 2: Extract Entities** → Pull details from B/L, Invoice, Packing List
3. **Node 3: Check Amount** → Amount ≤ LC amount? (Art. 18)
4. **Node 4: Check Quantity** → Quantity ≤ LC quantity? (Art. 18)
5. **Node 5: Check Description** → Use embeddings (text-embedding-3-small) to compare descriptions
6. **Node 6: Check Dates** → Shipment within LC period? On-board date before expiry?
7. **Node 7: ISBP 745 Reasoning** → Apply ISBP 745 rules for any marginal cases
8. **Node 8: Consolidate & Report** → Final verdict with reasoning

**State Management:**
```python
class LCCheckState(TypedDict):
    lc_data: dict
    invoice_data: dict
    bl_data: dict
    packing_list_data: dict
    discrepancies: list[str]
    compliances: list[str]
    isbp_notes: list[str]
    final_verdict: str  # "COMPLIANT", "DISCREPANCY", "NEEDS_REVIEW"
```

**Why LangGraph?**
- **Cyclic Reasoning:** If description check fails, agent can loop back to re-examine with ISBP 745 context
- **State Persistence:** All data flows through single state object (unlike multi-agent with message passing)
- **Deterministic + Flexible:** Nodes are deterministic (math, string matching), but can branch on semantic reasoning

---

## Next Steps

1. **Download 3 mock LC sets** (see `/mock_documents/` folder)
2. **Run extraction tools** on each PDF (we'll build these next)
3. **Test the compliance checker** with intentional discrepancies
4. **Iterate on ISBP 745 rules** based on test results

---

**References:**
- UCP 600: International Chamber of Commerce Uniform Customs and Practice for Documentary Credits
- ISBP 745: International Standard Banking Practice for the Examination of Documents under Documentary Credits
- Standard Chartered Bank Trade Finance Guidelines
