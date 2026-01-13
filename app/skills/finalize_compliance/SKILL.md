# Finalize Compliance Skill (LC Transactions)

This Agent Skill is responsible for **aggregating** the outputs of specialist agents (B/L Expert, Invoice Expert, Packing List Expert, etc.) and producing a single, human-readable compliance verdict for a Letter of Credit transaction.

The design follows Anthropic's Agent Skills pattern: a folder that contains instructions, forms, references, and scripts that an agent can "enter" and use when it needs to finalize a compliance decision.

## What this skill does

- Reads all validation results produced by upstream skills.
- Weighs discrepancies vs compliant checks at the transaction level.
- Emits a `final_verdict` and explanatory `reasoning` string that can be shown directly to a human.

## Files in this folder

- `SKILL.md` – high‑level instructions and usage for agents.
- `forms.md` – input and output schemas this skill expects.
- `reference.md` – LC/UCP/ISBP references that should guide judgment.
- `scripts/finalize_compliance.py` – Python implementation of the aggregation logic for this skill.

## How agents should use this skill

1. Collect all `validation_results` emitted by specialist skills (each result should include `check`, `doc`, `status`, and `reason`).
2. Call the function `finalize_compliance_from_results` in `scripts/finalize_compliance.py` with the full list.
3. Use the returned `final_verdict` and `reasoning` as the authoritative compliance outcome for the workflow.

This keeps the "decision policy" for compliance centralized in a dedicated Agent Skill instead of being scattered as hard-coded logic in the orchestration layer.
