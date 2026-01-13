# Finalize Compliance – Reference

This skill should apply the same professional standards a human trade finance officer would use when deciding whether an LC presentation is compliant.

## Core standards

- **UCP 600 Article 14** – Banks must examine documents with reasonable care and determine on the basis of the documents alone whether they appear on their face to constitute a complying presentation.
- **UCP 600 Article 18** – Invoice descriptions must "correspond" with the LC but may contain additional details that do not conflict with the LC.
- **ISBP 745 (including Article E26)** – Transport documents such as Bills of Lading may describe goods in more general terms, as long as they are not inconsistent with the LC.

## Project-specific guidance

- The **PICK strategy** in `docs/PICK_STRATEGY.md` separates Tier 1 (critical, payment‑blocking) checks from Tier 2 (important, discrepancy‑flagging) checks.
- The mock datasets in `mock_documents/` include realistic edge cases (generic B/L descriptions, special conditions, and shipment restrictions) that this skill should handle consistently.

## Decision philosophy

When aggregating results:

- If **any Tier 1 check** fails (for example, expiry, amount, ports, shipment dates), the safest default is a **Discrepant** verdict.
- If only Tier 2 checks fail (for example, some description or documentation nuances), a future version of this skill could emit a softer state such as `"Minor_Discrepancy"` or suggest a waiver path.
- If no discrepancies are reported, the presentation should be considered **Compliant** and suitable for payment.

The current implementation in `scripts/finalize_compliance.py` focuses on cleanly summarizing the existing `validation_results`. The surrounding documentation ensures the policy can evolve without deeply changing orchestration code.
