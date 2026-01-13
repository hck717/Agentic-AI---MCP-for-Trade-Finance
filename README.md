# Agentic AI for Trade Finance Compliance 💁❤️🧐

**A Multi-Agent System for automating Letter of Credit (LC) compliance checking using LangGraph, MCP, and AI Agents.**

## 🚀 Project Overview (POC)

This project demonstrates how **Agentic AI** can solve the complexity of Trade Finance document examination. Specifically, it tackles the non-linear "human" reasoning required to handle discrepancies that strict rule-based systems often fail at.

### The "Tricky Discrepancy" Case
A classic compliance challenge is the **Description Mismatch**:
- **Letter of Credit (LC):** Requires "Apple iPhone 15 Pro Max smartphones".
- **Bill of Lading (B/L):** States "Electronic Devices - Apple iPhone".
- **Commercial Invoice:** States "Apple iPhone 15 Pro Max, 256GB, Space Black".

**The Problem:** A rigid string-matching algorithm would reject the B/L for not matching the LC exactly.
**The Solution:** This Agentic System uses **ISBP 745 Article E26**, which allows B/L descriptions to be in "general terms not inconsistent with the credit." The AI agents use semantic reasoning to understand that "Electronic Devices" is a valid generalization of "iPhone", resulting in a **Compliant** verdict.

---

## 🔒 Data Privacy & Security (100% Private)

This solution is designed for **Zero Data Leakage** architectures, making it suitable for strict banking environments.

### Why It's 100% Secure:
1.  **Local "Brain" (On-Premise AI):**
    *   The system uses **Ollama** running **Llama 3.2** entirely on your local machine.
    *   No data is ever sent to cloud providers; reasoning happens on your own hardware.
2.  **Air-Gap Capable:** Works entirely **offline** without external API calls.
3.  **Local Context Protocol:** Uses **MCP** to securely connect the AI to local mock databases and files without uploading them.

---

## 🧠 System Workflow: How It Works

The system follows a modular **"Plan-Execute-Review"** architecture orchestrated by **LangGraph**.

### 1. Planning Stage (The Analyst)
The **Planner Node** analyzes the SWIFT MT700 (LC) and identifies the required checks (e.g., ports, dates, descriptions). It assigns a unique **Evidence ID** (E1, E2, etc.) to every source document to ensure 100% traceability.

### 2. Execution Stage (The Specialists)
Specialized agents perform deep-dive validations:
- **B/L Expert:** Validates logistics (Port of Loading/Discharge) and shipment dates.
- **Invoice Expert:** Validates financial details and specific goods descriptions.
- **PL Expert:** Cross-checks cargo weights and packaging details between documents.

### 3. Review Stage (Evidence-Led Reasoning)
The **Reviewer Node** synthesizes all findings into a professional-grade report.
- **Citations:** Every claim is backed by inline citations (e.g., `[E1](#e1)`).
- **Appendix:** A generated **Evidence Appendix** maps citations to human-readable source descriptions.
- **Verdict:** Produces a final **Compliant** or **Discrepant** decision based on UCP 600 standards.

---

## 🏗️ Technical Stack

- **Orchestration:** [LangGraph](https://www.langchain.com/langgraph) (Stateful multi-agent flows)
- **AI Model:** [Llama 3.2](https://ollama.com/) (Local deployment via Ollama)
- **Protocol:** [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (Tool and data abstraction)
- **Standards:** UCP 600 & ISBP 745 (International banking compliance rules)
- **Interface:** Streamlit (Real-time agent thought visualization)

---

## ⚡ Quick Start

### Option 1: Run Locally (Streamlit UI) 🖥️

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hck717/Agentic-AI---MCP-for-Trade-Finance.git
    cd Agentic-AI---MCP-for-Trade-Finance
    ```

2.  **Set up Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Web App:**
    ```bash
    streamlit run app/ui/streamlit_app.py
    ```

### Option 2: Run with Docker 🐳
```bash
docker build -t trade-finance-agent .
docker run -p 8501:8501 trade-finance-agent
```
    1.  Go to the Sidebar in the Web App.
    2.  Change **Ollama API URL** from `http://localhost:11434/v1` to:
        ```
        http://host.docker.internal:11434/v1

---

## 📝 Documentation Resources

- **[PICK Strategy](docs/PICK_STRATEGY.md):** Data extraction strategy.
- **[Evidence Referencing](app/utils/referencing.py):** New professional reporting utility.
- **[Phase 2 Implementation](docs/PHASE_2_MCP_AGENTS.md):** Technical details of the Multi-Agent architecture.

---

**Author:** [hck717](https://github.com/hck717)
**License:** MIT
