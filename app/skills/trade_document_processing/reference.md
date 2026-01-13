# Trade Document Processing Skill – Reference

This skill encapsulates the domain knowledge needed to extract and validate key fields from core trade documents under a Letter of Credit (LC) transaction.

## Standards and Guides

- UCP 600 Articles 14 and 18 for document examination timelines and invoice description correspondence.
- ISBP 745, especially Article E26, for rules on generic descriptions on transport documents.
- Internal project docs in `docs/`:
  - `PICK_STRATEGY.md` for tiered field importance and validation flow.
  - `LC_TYPES_DETAILS_PARTIES.md` for LC structure, types, and party roles.
  - `IMPLEMENTATION_ROADMAP.md` for how this skill is wired into the wider agentic system.

## Documents Covered

- Letter of Credit (LC)
- Commercial Invoice
- Bill of Lading (B/L)
- Packing List

Each document is mapped into a structured Pydantic model (`LCData`, `InvoiceData`, `BLData`, `PackingListData`) before validation.

## Output Expectations

The scripts in `scripts/` must return small, self-contained result objects with:

- `check`: Name of the check performed.
- `doc`: Which document was checked.
- `status`: `"Compliant"` or `"Discrepant"`.
- `reason`: One-sentence explanation citing relevant business logic or standards.
