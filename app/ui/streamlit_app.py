import streamlit as st
import time
import sys
import os
import json

# --- Fix Python Path for Import ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.graph import build_graph

# --- Page Config ---
st.set_page_config(
    page_title="AI Trade Finance Agent",
    page_icon="🚢",
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .compliant {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .discrepant {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🚢 Agentic AI Trade Finance Compliance")
st.markdown("### Powered by LangGraph & MCP Skills")

# --- Sidebar (Configuration) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # 1. Scenario Selector
    scenario_option = st.selectbox(
        "Select Mock Scenario:",
        [
            "1. Apple iPhone Import (Large Corp)",
            "2. Vietnamese Silk (SME)",
            "3. Indian Auto Parts (Mid-size)"
        ]
    )
    
    # Map selection to ID
    scenario_map = {
        "1. Apple iPhone Import (Large Corp)": "apple",
        "2. Vietnamese Silk (SME)": "silk",
        "3. Indian Auto Parts (Mid-size)": "auto"
    }
    selected_scenario_id = scenario_map[scenario_option]

    st.markdown("---")
    st.header("🤖 AI Settings")
    
    # 2. Dynamic Ollama URL Configuration
    ollama_url = st.text_input(
        "Ollama API URL:", 
        value="http://localhost:11434/v1",
        help="Change this if your Ollama is running on a different port (e.g., :11435)"
    )
    
    st.markdown("---")
    st.header("📂 Document Check")
    st.checkbox("Letter of Credit (LC)", value=True, disabled=True)
    st.checkbox("Bill of Lading (B/L)", value=True, disabled=True)
    st.checkbox("Commercial Invoice", value=True, disabled=True)
    st.checkbox("Packing List (PL)", value=True, disabled=True)
    
    # Check Connection Button
    if st.button("🔄 Check Connection"):
         try:
            from openai import OpenAI
            tmp_client = OpenAI(base_url=ollama_url, api_key="ollama")
            tmp_client.models.list()
            st.success(f"Connected to {ollama_url}!")
         except Exception as e:
            st.error(f"Connection Failed: {e}")
            
    st.caption("v1.5.0 | Built by hck717")

# --- Initialize LLM Client ---
try:
    from openai import OpenAI
    client = OpenAI(
        base_url=ollama_url,
        api_key="ollama"
    )
    HAS_LLM = True
except Exception:
    HAS_LLM = False

def query_llm(user_query, context_data):
    """
    Uses local Llama 3.2 to answer questions based on the compliance check results.
    """
    if not HAS_LLM:
        return "⚠️ OpenAI SDK not found. Please install 'openai' package."

    system_prompt = f"""
    You are an expert Trade Finance Compliance Assistant.
    You have performed a compliance check on a Letter of Credit (LC) and a set of documents.
    
    Here is the detailed result of the check in JSON format:
    ```json
    {json.dumps(context_data, indent=2)}
    ```
    
    Your Goal: Answer the user's question accurately based ONLY on the provided JSON data.
    - If the user asks "Why failed?", look for "status": "Discrepant" in the results.
    - If the user asks about specific documents, check the "validation_results" list.
    - Be concise, professional, and explain the reasoning clearly using UCP 600 / ISBP 745 terminology if applicable.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3.2", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling Local LLM: {str(e)}. Ensure Ollama is running at {ollama_url} and 'llama3.2' is pulled."

# --- Scenario Info Box ---
if selected_scenario_id == "apple":
    st.info("""
    **Scenario: Apple iPhone Import**
    *   **LC:** "Apple iPhone 15 Pro Max smartphones"
    *   **B/L:** "Electronic Devices" (Generic)
    *   **Challenge:** Semantic matching (ISBP 745 Art. E26).
    """)
elif selected_scenario_id == "silk":
    st.info("""
    **Scenario: Vietnamese Silk Export**
    *   **LC:** "100% Silk Scarves"
    *   **B/L:** "Textile Products - Silk" (Generic)
    *   **Challenge:** Verify SME document consistency.
    """)
elif selected_scenario_id == "auto":
    st.info("""
    **Scenario: Indian Auto Parts**
    *   **LC:** "Automotive Transmission & Gearbox Parts"
    *   **B/L:** "Auto Parts" (Generic)
    *   **Challenge:** High-value industrial parts verification.
    """)

# --- Session State for Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "final_state" not in st.session_state:
    st.session_state.final_state = None
if "last_scenario" not in st.session_state:
    st.session_state.last_scenario = None

# Reset chat if scenario changes
if st.session_state.last_scenario != selected_scenario_id:
    st.session_state.messages = []
    st.session_state.final_state = None
    st.session_state.last_scenario = selected_scenario_id

# --- Main Action ---
if st.button("🚀 Start Compliance Check", type="primary"):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Agent Thought Process")
        planner_log = st.empty()
        bl_log = st.empty()
        inv_log = st.empty()
        pl_log = st.empty()
        review_log = st.empty()

    # Run the Graph with selected scenario
    workflow = build_graph()
    
    planner_log.info(f"🧠 **Planner:** Analyzing {selected_scenario_id.upper()} LC requirements...")
    time.sleep(1) 
    
    # PASS SCENARIO ID HERE
    final_state = workflow.invoke({"scenario_id": selected_scenario_id})
    st.session_state.final_state = final_state
    
    planner_log.success("🧠 **Planner:** Plan created! Delegating to Experts.")
    
    time.sleep(1)
    bl_log.info("🚢 **B/L Expert:** Checking Port, Date, and Description...")
    time.sleep(0.5)
    bl_log.success("🚢 **B/L Expert:** Checks complete.")

    time.sleep(1)
    inv_log.info("💰 **Invoice Expert:** Checking Amount and Description...")
    time.sleep(0.5)
    inv_log.success("💰 **Invoice Expert:** Checks complete.")
    
    time.sleep(1)
    pl_log.info("📦 **PL Expert:** Checking Weights and Cross-references...")
    time.sleep(0.5)
    pl_log.success("📦 **PL Expert:** Checks complete.")
    
    time.sleep(1)
    review_log.info("⚖️ **Reviewer:** Analyzing findings against UCP 600...")
    time.sleep(0.5)
    
    with col2:
        st.subheader("📝 Final Compliance Report")
        
        verdict = final_state["final_verdict"]
        reason = final_state["reasoning"]
        
        if verdict == "Compliant":
            st.markdown(f"""
            <div class="compliant">
                <h3>✅ VERDICT: COMPLIANT</h3>
                <p><strong>Reasoning:</strong> {reason}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
             st.markdown(f"""
            <div class="discrepant">
                <h3>❌ VERDICT: DISCREPANT</h3>
                <p><strong>Reasoning:</strong> {reason}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("#### 🔍 Detailed Findings")
        for res in final_state["validation_results"]:
            icon = "✅" if res["status"] == "Compliant" else "❌"
            with st.expander(f"{icon} [{res['doc']}] {res['check']}"):
                st.write(f"**Status:** {res['status']}")
                st.write(f"**Reason:** {res['reason']}")

    review_log.success("⚖️ **Reviewer:** Final Verdict Generated.")

# --- Chat Interface ---
st.markdown("---")
st.subheader("💬 AI Compliance Assistant")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the compliance check..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = ""
        state = st.session_state.final_state
        
        if not state:
            response = "Please run the compliance check first so I can analyze the documents."
        else:
            if HAS_LLM:
                # Prepare Context
                context = {
                    "scenario": selected_scenario_id,
                    "final_verdict": state["final_verdict"],
                    "reasoning": state["reasoning"],
                    "validation_details": state["validation_results"]
                }
                # Call LLM
                with st.spinner(f"Llama 3.2 is thinking (via {ollama_url})..."):
                    response = query_llm(prompt, context)
            else:
                response = "⚠️ Chat is disabled because 'openai' package is missing."
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
