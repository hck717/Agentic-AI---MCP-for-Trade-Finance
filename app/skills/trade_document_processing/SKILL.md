# Trade Finance Compliance Skill

This skill allows agents to process Trade Finance documents (Letter of Credit, Bill of Lading, Invoice) for compliance checking against UCP 600 and ISBP 745 standards.

## Capabilities

1.  **Extraction ("Pick"):** Extracts structured data from raw text/PDFs of trade documents.
2.  **Validation ("Execute"):** Performs rule-based and semantic checks to identify discrepancies.

## Usage

Agents should use the scripts in the `scripts/` directory to perform actions.

### 1. Data Extraction
Use `extraction.py` to parse documents into standardized schemas (`LCData`, `BLData`, `InvoiceData`).

```python
from app.skills.trade_document_processing.scripts.extraction import pick_lc_data, pick_bl_data
lc_data = pick_lc_data("path/to/lc.pdf")
```

### 2. Compliance Validation
Use `validation.py` to check for discrepancies.

```python
from app.skills.trade_document_processing.scripts.validation import execute_semantic_validation
result = execute_semantic_validation(lc_desc, bl_desc, doc_type="BL")
```

## Dependencies
- `pydantic`: For data validation.
- `app.models.schemas`: For shared data models.
