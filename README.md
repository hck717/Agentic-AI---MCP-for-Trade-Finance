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

## 🖥️ Web Interface Features (v1.1)

The project now includes a **Streamlit UI** to visualize the agent's reasoning process:

*   **🤖 Real-time Agent Thoughts:** Watch the **Planner**, **B/L Expert**, **Invoice Expert**, and **Packing List Expert** think and act in real-time.
*   **✅ Visual Verdict:** Clear Green (Compliant) or Red (Discrepant) report cards.
*   **🔍 Explainable AI:** Expandable sections showing the exact ISBP 745 rules applied.
*   **💬 AI Chat Assistant:** Ask questions like "Why is the weight compliant?" or "Why is the B/L accepted?" to get instant, context-aware answers.

---

## 🏗️ Architecture: Plan-Pick-Execute

The system uses a **ReAct Pattern** (Reasoning + Acting) orchestrated by **LangGraph**.

### 1. The Agents (The "Brain") 🧠
Located in `app/agents/graph.py`, the workflow consists of:
- **Planner Node:** Analyzes the LC to decide what needs checking.
- **B/L Expert:** Specialist agent that validates logistics data (Ports, Dates).
- **Invoice Expert:** Specialist agent that validates financial data (Amounts, Specific Descriptions).
- **Packing List Expert:** Cross-checks weights and package counts against B/L and Invoice.
- **Reviewer Node:** Synthesizes findings and checks for UCP 600 Art. 14 conflicts.

### 2. The Skills (The "Hands") 🛠️
Located in `app/skills/`, we use a modular **Agent Skill** structure:
- **Extraction:** Extracts structured data (LC, Inv, B/L, PL).
- **Validation:** Performs semantic logic (Description matching, Weight cross-check).

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
    👉 Access the UI at `http://localhost:8501`

### Option 2: Run with Docker 🐳

1.  **Build the Image:**
    ```bash
    docker build -t trade-finance-agent .
    ```

2.  **Run the Container:**
    ```bash
    docker run -p 8501:8501 trade-finance-agent
    ```
    👉 Access the UI at `http://localhost:8501`

---

## 📝 Documentation Resources

- **[PICK Strategy](docs/PICK_STRATEGY.md):** Detailed breakdown of data extraction strategy.
- **[LC Reference](docs/LC_TYPES_DETAILS_PARTIES.md):** Comprehensive guide to LC fields and parties.
- **[Phase 2 Implementation](docs/PHASE_2_MCP_AGENTS.md):** Technical details of the Multi-Agent architecture.

---

**Author:** [hck717](https://github.com/hck717)
**License:** MIT
