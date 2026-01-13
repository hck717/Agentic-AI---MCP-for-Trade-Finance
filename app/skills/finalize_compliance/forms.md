# Finalize Compliance – Forms

This skill expects and returns **structured JSON-like objects** so that both humans and agents can understand and modify the policy in one place.

## Input schema

The main input is a list named `validation_results`.

Each element should be an object with the following fields:

- `check`: string; name of the check performed (for example, `"Goods Description"`).
- `doc`: string; which document was checked (for example, `"Invoice"`, `"B/L"`, `"PackingList"`).
- `status`: string; MUST be either `"Compliant"` or `"Discrepant"`.
- `reason`: string; one- or two-sentence natural language explanation.

Example:

```json
[
  {
    "check": "Goods Description",
    "doc": "Invoice",
    "status": "Compliant",
    "reason": "Invoice description corresponds to LC description under UCP 600 Art. 18."
  },
  {
    "check": "Shipment Date",
    "doc": "B/L",
    "status": "Discrepant",
    "reason": "Shipped on board date is after the latest shipment date in the LC."
  }
]
```

## Output schema

The function `finalize_compliance_from_results` returns a single object with:

- `final_verdict`: string; `"Compliant"` or `"Discrepant"` for now.
- `reasoning`: string; multi-line explanation summarizing why the verdict was reached.

Example:

```json
{
  "final_verdict": "Discrepant",
  "reasoning": "1 discrepancies were reported by specialist agents.\n- B/L – Shipment Date: Shipped on board date is after the latest shipment date in the LC."
}
```

Agents should treat this output as the **authoritative** decision for the LC transaction and surface it directly in UI or downstream workflows.
