from typing import List, Dict

def generate_professional_report(
    final_verdict: str, 
    reasoning: str, 
    validation_results: List[dict], 
    evidence_map: Dict[str, str]
) -> str:
    """
    Generates a professional-grade report with inline citations and an evidence appendix.
    Inspired by FYP-Prep's evidence-led reasoning.
    """
    
    # 1. Header & Verdict
    status_icon = "✅" if final_verdict == "Compliant" else "❌"
    report = f"# 📄 Trade Finance Compliance Report\n\n"
    report += f"## ⚖️ Final Verdict: {status_icon} **{final_verdict.upper()}**\n\n"
    
    # 2. Reasoning Summary
    report += "### 🧠 Decision Rationale\n"
    report += f"{reasoning}\n\n"
    
    # 3. Detailed Validation Table with Citations
    report += "### 🔍 Validation Details\n"
    report += "| Status | Document | Check | Reason | Evidence |\n"
    report += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for res in validation_results:
        icon = "✅" if res.get("status") == "Compliant" else "❌"
        doc = res.get("doc", "Unknown")
        check = res.get("check", "Unknown")
        reason = res.get("reason", "N/A")
        
        # Build Citations (e.g., [E1](#e1))
        ev_ids = res.get("evidence_ids", [])
        citations = ", ".join([f"[{eid}](#{eid.lower()})" for eid in ev_ids]) if ev_ids else "-"
        
        report += f"| {icon} | {doc} | {check} | {reason} | {citations} |\n"
    
    # 4. Evidence Appendix
    report += "\n---\n\n## 📚 Evidence Appendix\n"
    if evidence_map:
        for eid, source in evidence_map.items():
            # Create an anchor for each item
            report += f"- <a id='{eid.lower()}'></a>**{eid}**: {source}\n"
    else:
        report += "- (No evidence records found)\n"
        
    report += "\n\n*Note: This report was generated using Evidence-Led Reasoning based on UCP 600 standards.*"
    
    return report
