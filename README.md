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

## 🏗️ Architecture: Plan-Pick-Execute

The system uses a **ReAct Pattern** (Reasoning + Acting) orchestrated by **LangGraph**.

### 1. The Agents (The "Brain") 🧠
Located in `app/agents/graph.py`, the workflow consists of:
- **Planner Node:** Analyzes the LC to decide what needs checking (e.g., "Check Port", "Check Description").
- **B/L Expert:** Specialist agent that validates logistics data (Ports, Dates).
- **Invoice Expert:** Specialist agent that validates financial data (Amounts, Specific Descriptions).
- **Reviewer Node:** Synthesizes findings and checks for UCP 600 Art. 14 conflicts.

### 2. The Skills (The "Hands") 🛠️
Located in `app/skills/`, we use a modular **Agent Skill** structure (inspired by Anthropic's PDF skills):

```text
app/skills/trade_document_processing/
├── SKILL.md          # Documentation & Usage Guide
├── rules.md          # Context (UCP 600 & ISBP 745 Knowledge)
└── scripts/          # Executable Python Logic
    ├── extraction.py # "Pick": Extracts data from docs
    └── validation.py # "Execute": Performs semantic logic
```

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
    Access the UI at `http://localhost:8501`

### Option 2: Run with Docker 🐳

1.  **Build the Image:**
    ```bash
    docker build -t trade-finance-agent .
    ```

2.  **Run the Container:**
    ```bash
    docker run -p 8501:8501 trade-finance-agent
    ```
    Access the UI at `http://localhost:8501`

---

## 📝 Documentation Resources

- **[PICK Strategy](docs/PICK_STRATEGY.md):** Detailed breakdown of data extraction strategy.
- **[LC Reference](docs/LC_TYPES_DETAILS_PARTIES.md):** Comprehensive guide to LC fields and parties.
- **[Phase 2 Implementation](docs/PHASE_2_MCP_AGENTS.md):** Technical details of the Multi-Agent architecture.

---

## 🛠️ Tech Stack

- **LangGraph:** For stateful, multi-agent orchestration.
- **Pydantic:** For strict data validation and standardized schemas.
- **Streamlit:** For the interactive web interface.
- **Python 3.11:** Core programming language.
- **Docker:** For containerized deployment.

---

**Author:** [hck717](https://github.com/hck717)
**License:** MIT
