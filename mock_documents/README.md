# Trade Finance Mock Documents

Comprehensive mock trade finance document sets for testing and training the Agentic AI Trade Finance Compliance Agent.

## Overview

This folder contains 3 complete trade finance transaction datasets, each including:
- **Letter of Credit (LC)** - The core trade finance instrument
- **Commercial Invoice** - Seller's billing document
- **Bill of Lading (B/L)** - Shipping document
- **Packing List** - Contents and packaging details

---

## Dataset 1: Apple iPhone Import (Large Corp - Electronics Retail)

**Folder:** `1_APPLE_IPHONE_IMPORT/`

**Transaction Details:**
- **Buyer:** TechWorld Distribution Ltd (Hong Kong)
- **Seller:** Apple Inc. (USA)
- **Sector:** Electronics Retail
- **LC Amount:** USD 500,000
- **Currency:** USD
- **Goods:** Apple iPhone 15 Pro Max smartphones (5,000 units)
- **Incoterms:** CIF Hong Kong
- **Ports:** Los Angeles → Hong Kong
- **Key LC Features:**
  - 10% tolerance plus / 5% tolerance minus
  - Certificate of Origin required
  - Insurance required (CIF terms)

**Use Cases:**
- High-value consumer electronics transaction
- Multi-item invoice (different storage capacities/colors)
- Large quantity shipment (100 cartons)
- Description hierarchy test (iPhone model vs "Electronic Devices" in B/L)

---

## Dataset 2: Vietnamese Silk Export (SME - Textile Manufacturing)

**Folder:** `2_TEXTILE_EXPORT/`

**Transaction Details:**
- **Buyer:** Fashion Plus GmbH (Germany)
- **Seller:** Vietnamese Silk Trading Co Ltd (Vietnam)
- **Sector:** Textile Manufacturing
- **LC Amount:** EUR 85,000
- **Currency:** EUR
- **Goods:** Silk scarves and textile products (10,000 pieces)
- **Incoterms:** FOB Ho Chi Minh City
- **Ports:** Ho Chi Minh City → Hamburg
- **Key LC Features:**
  - 5% tolerance both ways
  - Pre-shipment inspection mandatory
  - Certificate of Origin (Vietnam) required
  - Vietnam origin requirement (special condition)

**Use Cases:**
- Medium-value commodity export
- SME exporter scenario
- Pre-shipment inspection requirement
- Multiple SKUs with similar products
- Country-of-origin verification

---

## Dataset 3: Indian Automotive Parts (Mid-size - Manufacturing)

**Folder:** `3_AUTOMOTIVE_PARTS/`

**Transaction Details:**
- **Buyer:** Toyota Parts Australia Pty Ltd (Australia)
- **Seller:** Precision Manufacturing India Pvt Ltd (India)
- **Sector:** Automotive Parts Manufacturing
- **LC Amount:** AUD 250,000
- **Currency:** AUD
- **Goods:** Transmission components & gearbox parts (50,000 units)
- **Incoterms:** CIF Melbourne
- **Ports:** Chennai → Melbourne
- **Key LC Features:**
  - Tight tolerance (2% both ways)
  - ISO 9001 certification mandatory
  - Quality inspection report required
  - Partial shipments allowed (max 3)
  - Transhipment NOT allowed

**Use Cases:**
- High-precision manufacturing export
- Quality certification requirements
- Partial shipment handling
- Transhipment restriction (compliance test)
- B2B industrial parts transaction

---

## Document Structure

Each dataset is organized as:

```
mock_documents/
├── 1_APPLE_IPHONE_IMPORT/
│   ├── LC_LC-2026-001-HSBC.md                    # Letter of Credit
│   ├── INVOICE_INV-2026-00145.md                 # Commercial Invoice
│   ├── BL_MAEU123456789.md                       # Bill of Lading
│   └── PACKING_LIST_PL-2026-00145.md             # Packing List
├── 2_TEXTILE_EXPORT/
│   ├── LC_LC-2026-VN-STT.md
│   ├── INVOICE_VST-INV-2026-0089.md
│   ├── BL_VCTL202602001.md
│   └── PACKING_LIST_PL-VST-2026-0089.md
├── 3_AUTOMOTIVE_PARTS/
│   ├── LC_LC-2026-AU-PMI.md
│   ├── INVOICE_PMI-INV-AU-2026-0047.md
│   ├── BL_PMI-2026-BLG-001.md
│   └── PACKING_LIST_PL-PMI-AU-2026-047.md
└── README.md                                      # This file
```

---

## Document Types

### Letter of Credit (LC)

The core trade finance instrument that:
- Specifies the payment terms (USD/EUR/AUD amount)
- Details the goods description and quantity
- Lists required documents
- Sets shipment date and port requirements
- Includes special conditions (certificates, inspections, etc.)
- States applicant (buyer) and beneficiary (seller)
- Defines tolerance bands for amounts and quantities

**Key Fields:**
- `lc_number`, `issue_date`, `expiry_date`
- `applicant`, `beneficiary`
- `goods_description`, `quantity`
- `latest_shipment_date`, `port_of_loading`, `port_of_discharge`
- `required_documents`, `special_conditions`
- `tolerance_plus`, `tolerance_minus`

### Commercial Invoice

The seller's billing document that:
- Lists items with quantities and unit prices
- Shows total amount due
- References the LC number
- Details buyer and seller information
- Specifies payment terms and currency

**Key Fields:**
- `invoice_number`, `date`
- `seller`, `buyer`
- `items[]` with `description`, `quantity`, `unit_price`, `total`
- `subtotal`, `tax`, `total`
- `reference_lc`

### Bill of Lading (B/L)

The shipping document that:
- Proves the goods have been shipped
- Specifies vessel and voyage details
- Lists ports of loading and discharge
- Describes goods (often in generic terms per ISBP 745)
- Shows on-board date (shipment proof)
- References invoice and LC

**Key Fields:**
- `bl_number`, `on_board_date`
- `shipper`, `consignee`
- `vessel`, `voyage`
- `port_of_loading`, `port_of_discharge`
- `goods_description` (can be generic per ISBP 745)
- `quantity_description`, `number_of_packages`, `gross_weight_kg`

### Packing List

The detailed contents document that:
- Lists items by carton/package number
- Shows quantities per package
- Specifies weights and dimensions
- Cross-references invoice and B/L numbers
- Provides audit trail for logistics

**Key Fields:**
- `packing_list_number`, `date`
- `invoice_number`, `bl_number` (cross-references)
- `items[]` with `carton_numbers`, `description`, `quantity`, `weight`
- `total_cartons`, `total_gross_weight_kg`

---

## Compliance Testing Scenarios

### Dataset 1 (Apple): Description Matching

**Test:** Semantic similarity between:
- LC: "Apple iPhone 15 Pro Max smartphones"
- Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black" + "Apple iPhone 15 Pro Max, 512GB, Silver"
- B/L: "Electronic Devices - Apple iPhone smartphones"

**Expected Behavior:** Recognize hierarchy (specific invoice details, generic B/L per ISBP 745)

---

### Dataset 2 (Textile): Special Conditions

**Test:** Verify:
- Pre-shipment inspection certificate submitted?
- Certificate of Origin from Vietnam?
- Country-of-origin requirement satisfied?

**Expected Behavior:** Flag missing pre-shipment inspection if not attached

---

### Dataset 3 (Automotive): Transhipment Restriction

**Test:** Check:
- LC says "Transhipment not allowed"
- B/L shows direct Chennai → Melbourne
- No intermediate vessel notation

**Expected Behavior:** COMPLIANT (no transhipment detected)

---

## Amount & Tolerance Calculations

### Dataset 1 (Apple)
```
LC Amount:           USD 500,000
Tolerance Plus:      10% = USD 50,000
Maximum Acceptable:  USD 550,000
Tolerance Minus:     5% = USD 25,000
Minimum Acceptable:  USD 475,000

Invoice Total:       USD 520,000 ✓ (Within tolerance)
```

### Dataset 2 (Textile)
```
LC Amount:           EUR 85,000
Tolerance Plus:      5% = EUR 4,250
Maximum Acceptable:  EUR 89,250
Tolerance Minus:     5% = EUR 4,250
Minimum Acceptable:  EUR 80,750

Invoice Total:       EUR 85,000 ✓ (Exact match)
```

### Dataset 3 (Automotive)
```
LC Amount:           AUD 250,000
Tolerance Plus:      2% = AUD 5,000
Maximum Acceptable:  AUD 255,000
Tolerance Minus:     2% = AUD 5,000
Minimum Acceptable:  AUD 245,000

Invoice Total:       AUD 250,000 ✓ (Exact match)
```

---

## Testing the Agentic AI System

### Step 1: Load Documents
```python
from pathlib import Path
import json

# Load all documents for Dataset 1
dataset_path = Path('mock_documents/1_APPLE_IPHONE_IMPORT')
lc_file = dataset_path / 'LC_LC-2026-001-HSBC.md'
invoice_file = dataset_path / 'INVOICE_INV-2026-00145.md'
bl_file = dataset_path / 'BL_MAEU123456789.md'
packing_list_file = dataset_path / 'PACKING_LIST_PL-2026-00145.md'
```

### Step 2: Extract Data
```python
# Use MCP tools to extract data from markdown files
lc_data = extract_lc_requirements(lc_file)
invoice_data = extract_invoice_details(invoice_file)
bl_data = extract_bl_details(bl_file)
packing_list_data = extract_packing_list_details(packing_list_file)
```

### Step 3: Run Compliance Checks
```python
# Run Tier 1 validation
tier1_results = validate_tier1_checks(lc_data, invoice_data, bl_data)

# Run semantic matching
similarity_scores = semantic_matching(lc_data, invoice_data, bl_data)

# Generate compliance report
report = generate_compliance_report(tier1_results, similarity_scores)

print(report)
# Expected Output: COMPLIANT or [DISCREPANCY details]
```

---

## Notes for Developers

1. **All documents are samples** - Created for training and testing purposes
2. **Real dates in 2026** - Organized chronologically for testing date-based logic
3. **Multiple currencies** - USD, EUR, AUD for multi-currency testing
4. **Different commodities** - Electronics, textiles, automotive for sector diversity
5. **Varying complexity** - Simple (textile), medium (automotive), complex (electronics)
6. **ISBP 745 compliant** - Descriptions follow ISBP 745 standards
7. **Realistic amounts** - Based on actual trade finance typical values

---

## Integration Points

These documents are designed to work with:

- **Document extraction tools** (`extract_lc_requirements`, `extract_invoice_details`, etc.)
- **Semantic matching** (Text embeddings for description comparison)
- **ISBP 745 rule engine** (Apply standards-based compliance logic)
- **LangGraph workflow** (Multi-agent validation pipeline)
- **Compliance reporting** (Generate audit trails and verdicts)

---

**Last Updated:** 2026-01-13

**Status:** Complete dataset ready for integration testing
