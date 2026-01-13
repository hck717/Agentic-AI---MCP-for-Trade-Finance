from typing import List, Dict


def finalize_compliance_from_results(validation_results: List[dict]) -> Dict[str, str]:
    """Aggregate specialist agent results into a single verdict.

    Each element of ``validation_results`` is expected to have:
      - "check": str
      - "doc": str
      - "status": "Compliant" | "Discrepant"
      - "reason": str
    """
    if not validation_results:
        return {
            "final_verdict": "Discrepant",
            "reasoning": "No validation results were provided. Unable to determine compliance.",
        }

    discrepancies = [r for r in validation_results if r.get("status") == "Discrepant"]
    compliant = [r for r in validation_results if r.get("status") == "Compliant"]

    # If there are no discrepancies, mark as compliant and summarize the key checks.
    if not discrepancies:
        lines = [
            "All specialist agents reported compliant results for the submitted documents.",
        ]
        for r in compliant:
            lines.append(f"- {r['doc']} – {r['check']}: {r['reason']}")

        return {
            "final_verdict": "Compliant",
            "reasoning": "\n".join(lines),
        }

    # Otherwise, aggregate discrepancies into a clear explanation.
    lines = [f"{len(discrepancies)} discrepancies were reported by specialist agents."]
    for d in discrepancies:
        lines.append(f"- {d['doc']} – {d['check']}: {d['reason']}")

    return {
        "final_verdict": "Discrepant",
        "reasoning": "\n".join(lines),
    }
