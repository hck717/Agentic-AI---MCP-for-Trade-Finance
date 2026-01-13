# Letter of Credit (LC): Types, Details, and Parties

Comprehensive reference guide for all LC variations, structural details, and involved parties in trade finance.

---

## Part 1: LC Types Classification

### 1.1 By Revocability

#### Irrevocable LC
**Definition:** Cannot be cancelled or modified without consent of all parties (issuer, confirmer, beneficiary)

**Key Characteristics:**
- Binding commitment from issuing bank
- Cannot be recalled unilaterally
- Provides maximum security to beneficiary (seller)
- Standard in modern trade finance
- Complies with UCP 600

**When Used:** Almost all commercial transactions

**Example from Mock Data:**
```
LC/2026/001/HSBC - Apple iPhone Import
TC/2026/VN/STT - Vietnamese Silk Export
LC/2026/AU/PMI - Indian Automotive Parts
All are Irrevocable LCs
```

#### Revocable LC
**Definition:** Can be cancelled or modified by issuer without notice

**Key Characteristics:**
- Issuer can revoke anytime before payment
- No security for beneficiary
- Rarely used in modern practice
- Not recommended for international trade
- Legacy instrument (mostly historical)

**When Used:** Only in special cases of trust/related parties

**Risk Level:** HIGH for exporter

---

### 1.2 By Confirmation Status

#### Unconfirmed LC (LC Issued)
**Definition:** Bank's undertaking only (no additional confirmation)

**Parties:**
- Issuing Bank (responsible for payment)
- Beneficiary (relies on issuing bank's creditworthiness)

**Security Level:** Medium-High (depends on issuing bank's credit rating)

**Risk:** Country risk, issuing bank risk

**Typical Setup:**
```
Applicant (Buyer) 
    ↓
    Issues LC via Applicant's Bank (e.g., HSBC Hong Kong)
    ↓
    Transmits to Beneficiary (Seller)
    ↓
Beneficiary must trust Applicant's Bank
```

#### Confirmed LC (LC Issued + Confirmed)
**Definition:** Issuing bank's undertaking PLUS confirmation by another bank

**Parties:**
- Issuing Bank (original undertaking)
- Confirming Bank (adds its own commitment)
- Beneficiary (can claim from either bank)

**Security Level:** Very High

**Double Safety:**
1. Issuing bank's commitment
2. Confirming bank's commitment (additional layer)

**Typical Setup (Confirmed LC):**
```
Applicant (Buyer, e.g., TechWorld Dist Ltd)
    ↓
    Applies to Issuing Bank (HSBC HK)
    ↓
    Issuing Bank issues LC
    ↓
    Transmits to Confirming Bank (often local to beneficiary)
    ↓
    Confirming Bank confirms (adds its guarantee)
    ↓
    Beneficiary (Seller, e.g., Apple Inc.) receives confirmed LC
    ↓
    Beneficiary can claim payment from EITHER bank
```

**Why Confirm?**
- Removes issuing bank country risk
- Adds local bank's credit strength
- Improves payment certainty
- More expensive (additional bank fee)

**Cost:** Issuing fee (typically 0.5%-2%) + Confirmation fee (0.3%-0.7%)

---

### 1.3 By Presentation Requirements

#### Sight LC (at Sight)
**Definition:** Payment upon presentation of documents (immediate)

**Timeline:**
```
Beneficiary ships goods
    ↓
Beneficiary prepares documents
    ↓
Beneficiary presents documents to bank
    ↓
Bank checks documents for LC compliance (typically 5 banking days)
    ↓
[APPROVED] → Bank pays IMMEDIATELY (sight = at sight)
```

**Cash Flow:** Exporter gets paid fast

**All Mock Datasets:** "LC at sight" - beneficiary gets paid immediately upon document presentation

#### Time LC (Usance LC)
**Definition:** Payment on a future date (e.g., 30/60/90 days after presentation)

**Timeline:**
```
Beneficiary presents documents
    ↓
Bank approves documents
    ↓
Bank issues TIME DRAFT (e.g., "payable 60 days after sight")
    ↓
Beneficiary holds draft or sells it in money market
    ↓
60 days pass
    ↓
Applicant (importer) pays bank
    ↓
Bank pays beneficiary (or beneficiary's bank)
```

**Purpose:** Gives importer time to sell goods, generate cash, and pay

**Cost to Buyer:** Slightly cheaper than sight (issuing bank holds funds longer)

**Risk to Seller:** Must wait for payment

#### Negotiation LC
**Definition:** Beneficiary can negotiate (sell) the LC with any bank

**Key Feature:** "Freely negotiable" clause allows beneficiary to present at any bank

**Advantage:** More liquidity for beneficiary

---

### 1.4 By Coverage

#### Sight LC (Full Coverage)
**Definition:** LC amount covers full invoice total

**Example (Dataset 1):**
```
LC Amount:       USD 500,000
Invoice Total:   USD 520,000
[PROBLEM] Invoice exceeds LC!

But tolerance plus 10% = USD 50,000 allowed
520,000 - 500,000 = 20,000 ✓ Within 10% tolerance
```

#### Revolving LC
**Definition:** Amount automatically replenishes after payment

**Use Case:** For multiple shipments over time

**Example:**
```
LC Amount:       USD 100,000 (monthly revolving)
Month 1: Ship $100k, LC expires
Month 2: LC automatically renews to $100k
Month 3: LC automatically renews to $100k
(Assuming terms allow revolving)
```

**Not in Mock Datasets** (single shipment each)

---

### 1.5 By Transferability

#### Transferable LC
**Definition:** Beneficiary can transfer rights to another party (sub-contractor, supplier)

**Scenario:**
```
Buyer → issues LC to → Beneficiary (middleman/trader)
    ↓
Beneficiary transfers LC to → Actual Supplier
    ↓
Supplier ships goods and gets paid
```

**Common in:** Trading chains, distribution networks

#### Non-Transferable LC
**Definition:** Only named beneficiary can claim payment

**Most LCs are non-transferable by default** (unless stated otherwise)

**In Mock Datasets:** All non-transferable (single named beneficiary)

---

### 1.6 By Payment Source

#### Regular LC (Documentary LC)
**Definition:** Payment dependent on satisfactory documents

**All Mock Datasets use Regular LC** - payment requires:
- Commercial Invoice
- Bill of Lading
- Packing List
- Certificates (origin, quality, inspection, insurance, etc.)

#### Stand-by LC
**Definition:** Like insurance - payment only if primary obligation is NOT met

**Scenario:**
```
Buyer purchases $100k equipment on credit (60-day terms)
Buyer's bank issues Stand-by LC for $100k
If buyer doesn't pay in 60 days → Seller calls Stand-by LC
Stand-by LC pays seller immediately
```

**Purpose:** Guarantees payment if buyer defaults on primary obligation

**Not in Mock Datasets** (all are documentary LCs)

---

## Part 2: LC Structural Details

### 2.1 Essential Fields

#### Field 20 - Bank Reference Number
```
Example: LC/2026/001/HSBC
Format: Issuing Bank's unique reference
Uniqueness: Unique per LC
Purpose: Identification and tracking
```

#### Field 31 - Date of Issue
```
Example: 2025-12-01
Format: YYYY-MM-DD
Purpose: Establishes LC validity start date
Important For: Determining if documents are presented in time
```

#### Field 31D - Date of Expiry
```
Example: 2026-02-15
Format: YYYY-MM-DD
Purpose: Deadline for presentation of documents
Critical For: If expired, documents cannot be claimed
Best Practice: Set to ~30 days after latest shipment date
```

#### Field 32 - Amount
```
Example: 500000 USD
Format: [Amount] [Currency]
Importance: Cannot be exceeded (except for tolerance)
Tolerance Rules:
  - Plus tolerance: Allows invoice to exceed by %
  - Minus tolerance: Allows invoice to be less than %
  - Standard: 5-10% plus, 2-5% minus

Calculation (Dataset 1):
  LC Amount:           USD 500,000
  Tolerance Plus:      10%
  Maximum Invoice:     USD 550,000 ✓
  
  Invoice Total:       USD 520,000 ✓ (Acceptable)
```

#### Field 43 - Form of Documentary Credit
```
Examples:
  - Irrevocable
  - Irrevocable Confirmed
  - Revocable (rare)
  
Mock Datasets: All "Irrevocable Confirmed"
Standard Default: Irrevocable (if not stated)
```

#### Field 44 - Form of Payment
```
Examples:
  - Sight (immediate payment)
  - 30 days after sight
  - 60 days after Bill of Lading date
  
Mock Datasets: "Sight payment" (immediate)
```

#### Field 46 - Documents Required

**Field 46A: Documents to be presented by the beneficiary**
```
Example Structure:
  46A: Commercial Invoice in triplicate
       Bill of Lading marked "Shipped on Board"
       Packing List
       Certificate of Origin
       Insurance Certificate (if CIF terms)
       
Each field lists specific requirements
```

**Field 46B: Additional required conditions**
```
Example:
  Pre-shipment inspection certificate
  Quality certificate
  Inspection for damage (on goods received)
  
Conditions must be satisfied BEFORE payment
```

**Field 46C: Goods Description**
```
Example:
LC Description: "Apple iPhone 15 Pro Max smartphones"

Allowed Variations (per ISBP 745):
Invoice: "Apple iPhone 15 Pro Max, 256GB, Space Black"
         (More specific - OK)
B/L:     "Electronic Devices - Apple iPhone"
         (More generic - OK per ISBP 745 Art. E26)

Hierarchy:
  General → Specific → Generic (all acceptable)
  "Electronic Devices" → "iPhone" → "iPhone 15 Pro Max, 256GB, Space Black"
```

#### Field 47 - Additional Conditions
```
Example (Dataset 1 - Apple):
  - Certificate of Origin required
  - Insurance with Certificate required (CIF terms)
  - Invoice must show full product specifications
  
Example (Dataset 3 - Automotive):
  - ISO 9001 certification mandatory
  - Quality inspection report required
  - Partial shipments allowed (max 3)
  - Transhipment not allowed
  
Importance: BLOCKING conditions
             If not satisfied = DISCREPANCY
             Payment may be withheld until resolved
```

#### Field 48 - Stating of Drawee
```
Example: "At the counters of [Bank Name]"
Meaning: Where beneficiary presents documents to get paid
Typical: Issuing Bank or Confirming Bank
```

#### Field 50 - Applicant
```
Example:
  Name: TechWorld Distribution Ltd
  Address: Tsuen Wan, Hong Kong
  
Role: BUYER (importer of goods)
Pays: The issuing bank upon LC maturity
Issues: The LC through their bank
```

#### Field 59 - Beneficiary
```
Example:
  Name: Apple Inc.
  Address: Cupertino, California, USA
  
Role: SELLER (exporter of goods)
Receives: Payment upon document presentation
Must Named: Exactly as stated in LC
            (or authorized agent)
```

---

### 2.2 Shipping Terms Fields

#### Incoterms (Responsibility & Cost Split)

**Field 39A/39B - Shipped on Board Period**
```
Example: "From 2025-12-01 to 2026-01-31"
Meaning: Goods must be loaded on vessel between these dates
Checked Against: B/L on-board date

Dataset 1 (Apple):
  Latest Shipment: 2026-01-31
  B/L On-Board Date: 2026-01-20 ✓ (In time)
```

**Incoterms Examples in Mock Data:**

| Dataset | Incoterms | Meaning | Seller Responsibility |
|---------|-----------|---------|------------------------|
| **Apple** | CIF Hong Kong | Cost, Insurance, Freight to HK | Pay shipping + insurance |
| **Textile** | FOB Ho Chi Minh City | Free on Board (at loading port) | Pay until goods loaded |
| **Automotive** | CIF Melbourne | Cost, Insurance, Freight to Melbourne | Pay shipping + insurance |

**CIF Terms (Datasets 1 & 3):**
- Seller pays shipping freight
- Seller obtains insurance
- Goods delivered to named port
- **Insurance Certificate Required** in documents

**FOB Terms (Dataset 2):**
- Seller pays until goods loaded
- Buyer pays freight from loading port onward
- Buyer arranges insurance (if needed)
- **Insurance Certificate Optional** (buyer arranges)

#### Ports

**Field 39B - Port of Loading**
```
Dataset 1: "Port of Los Angeles"
Dataset 2: "Port of Ho Chi Minh City"
Dataset 3: "Port of Chennai"

Matched in B/L: Must match exactly (or semantic match)
Allowed Variations (ISBP 745):
  LC: "Port of Los Angeles"
  B/L: "Los Angeles" ✓ (Acceptable)
  B/L: "Los Angeles, USA" ✓ (Acceptable)
  B/L: "Port of Oakland" ✗ (Different port - DISCREPANCY)
```

**Field 39D - Port of Discharge**
```
Dataset 1: "Port of Hong Kong"
Dataset 2: "Port of Hamburg"
Dataset 3: "Port of Melbourne"

Matched in B/L: Must match loading and discharge ports
Checkpoint: Is goods going to correct destination?
```

---

## Part 3: LC Parties and Their Roles

### 3.1 Primary Parties (Always Present)

#### 1. Applicant (Buyer/Importer)

**Definition:** Party requesting LC issuance (buyer of goods)

**Responsibilities:**
- Applies to their bank to issue LC
- Pays the issuing bank when documents presented
- Bears ultimate payment liability
- Provides funds to issuing bank

**Mock Examples:**
- **Dataset 1:** TechWorld Distribution Ltd (Hong Kong)
  - Importing iPhones from Apple
  - Applies to HSBC Hong Kong for LC
  - Pays HSBC when documents approved
  
- **Dataset 2:** Fashion Plus GmbH (Germany)
  - Importing silk from Vietnam
  - Applies to Techcombank for LC
  - Pays Techcombank when documents approved
  
- **Dataset 3:** Toyota Parts Australia Pty Ltd (Australia)
  - Importing parts from India
  - Applies to ICICI Bank for LC
  - Pays ICICI when documents approved

**Rights:**
- Can request documents be checked
- Can reject non-compliant documents
- Can waive discrepancies (if beneficiary agrees)

**Payment Flow:**
```
Applicant
    ↓
    Arranges credit facility with Issuing Bank
    Pays bank's LC issuance fees (0.5%-2%)
    ↓
    Receives LC (via bank)
    ↓
    Sends LC to Beneficiary
    (Beneficiary begins shipping)
    ↓
    [After shipment]
    Bank presents documents
    ↓
    [If documents compliant]
    Applicant reimburses Issuing Bank
    ↓
    Bank pays Beneficiary
```

---

#### 2. Beneficiary (Seller/Exporter)

**Definition:** Party entitled to payment (seller of goods)

**Responsibilities:**
- Ships goods as per LC terms
- Prepares required documents
- Presents documents within expiry date
- Must satisfy LC conditions

**Mock Examples:**
- **Dataset 1:** Apple Inc. (USA)
  - Exports iPhones to Hong Kong
  - Ships by Latest Shipment Date: 2026-01-31
  - Prepares Invoice, B/L, Packing List, Certificates
  - Presents documents to bank
  
- **Dataset 2:** Vietnamese Silk Trading Co Ltd (Vietnam)
  - Exports silk to Germany
  - Ships by Latest Shipment Date: 2026-02-15
  - Must obtain pre-shipment inspection cert
  - Must show Vietnam origin
  
- **Dataset 3:** Precision Manufacturing India Pvt Ltd (India)
  - Exports automotive parts to Australia
  - Ships by Latest Shipment Date: 2026-02-28
  - Must provide ISO 9001 certification
  - Must include quality inspection report

**Rights:**
- Entitled to payment if documents comply
- Can claim from issuing bank or confirming bank (if confirmed)
- Cannot be forced to accept discrepancies
- Can negotiate terms before shipment

**Payment Timeline:**
```
Beneficiary (Seller)
    ↓
Ships goods (on-board date)
    ↓
Prepares documents
  - Invoice
  - Bill of Lading (original + copies)
  - Packing List
  - Required certificates (origin, inspection, quality, insurance)
    ↓
Presents documents to bank
(within LC expiry date)
    ↓
Bank checks documents for LC compliance
(typically 5 banking days per UCP 600)
    ↓
[If COMPLIANT]
    Bank notifies applicant
    Bank pays beneficiary
    ↓
[If DISCREPANCY]
    Bank requests applicant waiver
    If approved → pays beneficiary
    If rejected → documents refused
```

---

### 3.2 Banking Parties (Intermediaries)

#### 1. Issuing Bank

**Definition:** Bank that issues LC on behalf of applicant

**Role:**
- Issues LC on applicant's request
- Examines documents for LC compliance
- Makes payment to beneficiary if documents OK
- Recovers funds from applicant

**Mock Examples:**
- **Dataset 1:** HSBC Bank Hong Kong
  - Issues LC/2026/001/HSBC for USD 500,000
  - Checks Apple's documents
  - Pays Apple if documents compliant
  - Collects payment from TechWorld Dist Ltd
  
- **Dataset 2:** Viet Nam Technological Bank (Techcombank)
  - Issues LC/2026/VN/STT for EUR 85,000
  - Checks Vietnamese Silk Trading's documents
  - Pays Vietnamese Silk if documents compliant
  - Collects payment from Fashion Plus GmbH
  
- **Dataset 3:** ICICI Bank Limited
  - Issues LC/2026/AU/PMI for AUD 250,000
  - Checks Precision Manufacturing's documents
  - Pays Precision Manufacturing if documents compliant
  - Collects payment from Toyota Parts Australia

**Responsibility:**
- Binding commitment to pay if documents are in order
- Cannot refuse payment for "good" reasons (only LC compliance)
- Standard of examination: reasonable care
- Timeline: Examine within 5 banking days (UCP 600 Art. 14)

**Liability:**
- Liable to beneficiary if wrongfully rejects compliant documents
- Not liable if documents don't comply with LC

---

#### 2. Confirming Bank (If Confirmed LC)

**Definition:** Bank that adds its own commitment to issuing bank's LC

**Role:**
- Receives LC from issuing bank
- Adds confirmation (own commitment to pay)
- Beneficiary can claim from confirming bank directly
- Does not need to go through issuing bank

**Scenario (if Dataset 1 was Confirmed):**
```
Issuing Bank: HSBC Hong Kong (issues LC)
    ↓
    Sends LC to Confirming Bank (e.g., Bank of America NY)
    ↓
Confirming Bank: Bank of America
    Adds confirmation
    Sends confirmed LC to Apple
    ↓
Apple can now:
  Option 1: Present documents to Bank of America (confirming bank)
  Option 2: Present documents to HSBC (issuing bank)
  
Either bank MUST pay if documents comply
```

**Why Confirm?**
- Adds second bank's creditworthiness
- Eliminates country risk of issuing bank's country
- Increases payment certainty
- Typical in international trade

**Cost:** Issuing bank pays confirming bank a confirmation fee (0.3%-0.7%)

**All Mock Datasets:** State "Irrevocable Confirmed LC" but don't explicitly name confirming bank (simplified)

---

#### 3. Negotiating Bank

**Definition:** Bank that negotiates (buys) LC documents from beneficiary

**Scenario:**
```
Beneficiary (seller) presents documents to Negotiating Bank
    ↓
Negotiating Bank:
  1. Checks documents for LC compliance
  2. Advances funds to beneficiary (buys the documents)
  3. Sends documents to issuing bank for reimbursement
    ↓
Issuing Bank:
  1. Checks documents again
  2. Reimburses negotiating bank
    ↓
Result: Beneficiary gets paid early (doesn't wait for issuing bank)
```

**Benefit:** Beneficiary gets paid immediately (negotiating bank doesn't wait)

**Common in:** International trade where beneficiary needs fast cash

---

### 3.3 Supporting Parties (Conditional)

#### 1. Inspector/Certifying Party

**Definition:** Third-party inspector for goods quality/quantity

**Used When:**
- Pre-shipment inspection required (Dataset 2 - Textile)
- Quality certification mandatory (Dataset 3 - Automotive)
- Goods valuation needed (high-value commodities)

**Role:**
- Inspects goods before/after loading
- Issues inspection certificate
- Required document for payment

**Dataset 2 Example:**
```
LC Special Conditions:
  "Pre-shipment inspection mandatory"
  
Required Documents:
  - Pre-shipment Inspection Certificate
  
Inspector: (Typically SGS, Bureau Veritas, TÜV)
Checks: Quality, quantity, packaging, specifications
Certifies: Goods comply with invoice
```

**Dataset 3 Example:**
```
LC Special Conditions:
  "ISO 9001 certification mandatory"
  "Quality inspection report required"
  
Certifier: Precision Manufacturing's Quality Dept
Checks: Parts meet ISO 9001 standards
Certifies: Manufacturing quality compliant
```

---

#### 2. Insurance Company

**Definition:** Insures goods in transit (for CIF terms)

**Used When:**
- CIF Incoterms (seller pays insurance)
- LC requires insurance certificate

**Mock Examples:**
- **Dataset 1 (Apple - CIF):** Insurance required
  - Seller (Apple) obtains insurance
  - Includes insurance certificate in documents
  - Covers goods Los Angeles → Hong Kong
  
- **Dataset 3 (Automotive - CIF):** Insurance required
  - Seller (Precision Mfg) obtains insurance
  - Covers goods Chennai → Melbourne
  
- **Dataset 2 (Textile - FOB):** Insurance optional
  - Buyer (Fashion Plus) would arrange insurance
  - Not part of LC documents

**Insurance Certificate Details:**
- Amount: Usually 110% of invoice value (covers claims + expense)
- Coverage: All-risks (or named perils)
- Beneficiary: Usually the buyer (applicant)
- Valid: From port of loading to final destination

---

#### 3. Shipping Line / Vessel Operator

**Definition:** Entity that transports goods via sea

**Role:**
- Issues Bill of Lading
- Loads goods on vessel
- Marks goods with on-board date
- Delivers goods to destination port

**Mock Examples:**
- **Dataset 1:** Maersk Line (MSC GULSUN, Voyage 219S)
- **Dataset 2:** ONE Line (ONE INNOVATION, Voyage 235N)
- **Dataset 3:** Evergreen Line (EVERGREEN, Voyage 2242E)

**B/L Role:**
- Proof of shipment
- Receipt of goods
- Contract of carriage
- Title document (can be traded)

---

## Part 4: Compliance Checklist

### Quick Reference: LC Compliance Review

**TIER 1 - CRITICAL (Block Payment if Failed)**

- [ ] **Expiry Date Check**
  - Has LC expired?
  - Expected: `Today <= Expiry_Date`
  - Dataset 1: Expires 2026-02-15 ✓
  
- [ ] **Currency Match**
  - LC Currency = Invoice Currency = B/L Currency?
  - Dataset 1: All USD ✓
  - Dataset 2: All EUR ✓
  - Dataset 3: All AUD ✓
  
- [ ] **Amount Check**
  - Invoice Total <= LC Amount × (1 + Tolerance_Plus)?
  - Dataset 1: 520,000 <= 550,000 (10% tolerance) ✓
  - Dataset 2: 85,000 <= 89,250 (5% tolerance) ✓
  - Dataset 3: 250,000 <= 255,000 (2% tolerance) ✓
  
- [ ] **Quantity Check**
  - B/L Quantity <= LC Quantity × (1 + Tolerance_Plus)?
  - Dataset 1: 5000 units <= 5500 units ✓
  
- [ ] **Shipment Date Check**
  - B/L On-Board Date <= LC Latest Shipment Date?
  - Dataset 1: 2026-01-20 <= 2026-01-31 ✓
  - Dataset 2: 2026-02-13 <= 2026-02-15 ✓
  - Dataset 3: 2026-02-24 <= 2026-02-28 ✓
  
- [ ] **Port Matching**
  - LC Loading Port ~ B/L Loading Port?
  - LC Discharge Port ~ B/L Discharge Port?
  - Allow abbreviations, country additions (ISBP 745)
  
- [ ] **Party Names**
  - Applicant name in Invoice Buyer Name?
  - Beneficiary name in Invoice Seller Name?
  - Fuzzy matching acceptable (slight variations OK)

**TIER 2 - IMPORTANT (Flag Discrepancy if Failed)**

- [ ] **Document Completeness**
  - All required documents present?
  - Dataset 1 requires: Invoice, B/L, Packing List, Certificate of Origin
  - Dataset 2 requires: Invoice, B/L, Packing List, Cert of Origin, Pre-shipment Inspection Cert
  - Dataset 3 requires: Invoice, B/L, Packing List, ISO 9001 Cert, Insurance Cert
  
- [ ] **Special Conditions Met**
  - Dataset 1: Certificate of Origin ✓, Insurance ✓, Full Specs ✓
  - Dataset 2: Pre-shipment Inspection ✓, Vietnam Origin ✓
  - Dataset 3: ISO 9001 ✓, Quality Report ✓, No Transhipment ✓
  
- [ ] **Description Matching**
  - Invoice description more specific than B/L? (OK per ISBP 745)
  - B/L description at least as general as LC? (OK per ISBP 745 Art. E26)
  - Semantic similarity > threshold (0.70-0.85)?
  
- [ ] **Document Cross-References**
  - Invoice # referenced in B/L? (if required)
  - B/L # referenced in Packing List? (if required)
  - LC # referenced in Invoice? (if required)

---

## Part 5: Summary Table

| Aspect | Dataset 1 (Apple) | Dataset 2 (Textile) | Dataset 3 (Automotive) |
|--------|-------------------|---------------------|------------------------|
| **LC Number** | LC/2026/001/HSBC | LC/2026/VN/STT | LC/2026/AU/PMI |
| **Type** | Irrevocable Confirmed | Irrevocable Confirmed | Irrevocable Confirmed |
| **Payment** | Sight | Sight | Sight |
| **Amount** | USD 500,000 | EUR 85,000 | AUD 250,000 |
| **Tolerance** | ±10%/5% | ±5% | ±2% |
| **Incoterms** | CIF Hong Kong | FOB Ho Chi Minh | CIF Melbourne |
| **Applicant** | TechWorld Dist | Fashion Plus GmbH | Toyota Parts Aus |
| **Beneficiary** | Apple Inc | Vietnam Silk Trading | Precision Mfg India |
| **Goods** | iPhone 15 Pro Max | Silk scarves | Auto transmission parts |
| **Quantity** | 5000 units | 10000 pieces | 50000 units |
| **Shipment Date** | 2026-01-20 | 2026-02-13 | 2026-02-24 |
| **Latest Date** | 2026-01-31 | 2026-02-15 | 2026-02-28 |
| **Key Condition** | Origin Cert + Insurance | Pre-shipment Inspect | ISO 9001 + Quality Rpt |
| **Test Focus** | Description hierarchy | Special conditions | Restrictions (tranship) |

---

**Reference Complete.** Ready for LC compliance checking! 🎯
