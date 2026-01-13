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
    *   No data is ever sent to OpenAI, Google, or any cloud provider.
    *   The "reasoning" happens on your own CPU/GPU.

2.  **Air-Gap Capable:**
    *   The entire application (Streamlit UI, Python Logic, AI Model) works **offline**.
    *   You can disconnect your internet, and the compliance check will still function perfectly.

3.  **No External API Calls:**
    *   Document extraction and validation logic (`validation.py`) are pure local Python scripts.
    *   No sensitive Letter of Credit data ever traverses the public internet.

*Compliance Ready: Meets strict data residency and banking secrecy requirements by bringing the AI to the data, not the data to the AI.*

---

## 🖥️ Web Interface Features (v1.5)

The project includes a **Streamlit UI** to visualize the agent's reasoning process:

*   **🤖 Real-time Agent Thoughts:** Watch the **Planner**, **B/L Expert**, **Invoice Expert**, and **Packing List Expert** think and act in real-time.
*   **✅ Visual Verdict:** Clear Green (Compliant) or Red (Discrepant) report cards.
*   **🔍 Explainable AI:** Expandable sections showing the exact ISBP 745 rules applied.
*   **💬 Local AI Chat (Ollama):** Ask questions like "Why did the Invoice fail?" using your local Llama 3.2 model. No data leaves your machine!

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
    # For Mac/Windows (Ollama on host):
    docker run -p 8501:8501 trade-finance-agent
    
    # For Linux (Ollama on host):
    docker run -p 8501:8501 --add-host=host.docker.internal:host-gateway trade-finance-agent
    ```

3.  **Connecting to Ollama from Docker:**
    If you see `🔴 Ollama Connection Failed` inside the Docker app:
    1.  Go to the Sidebar in the Web App.
    2.  Change **Ollama API URL** from `http://localhost:11434/v1` to:
        ```
        http://host.docker.internal:11434/v1
        ```
    3.  Click **🔄 Check Connection**.

    *Why? `localhost` inside Docker refers to the container itself, not your computer. `host.docker.internal` is the special address to reach your host machine.*

---

## 📝 Documentation Resources

- **[PICK Strategy](docs/PICK_STRATEGY.md):** Detailed breakdown of data extraction strategy.
- **[LC Reference](docs/LC_TYPES_DETAILS_PARTIES.md):** Comprehensive guide to LC fields and parties.
- **[Phase 2 Implementation](docs/PHASE_2_MCP_AGENTS.md):** Technical details of the Multi-Agent architecture.

---

**Author:** [hck717](https://github.com/hck717)
**License:** MIT
