import streamlit as st
import time
import sys
import os

# --- Fix Python Path for Import ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.graph import build_graph

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
    st.header("📂 Document Check")
    st.checkbox("Letter of Credit (LC)", value=True, disabled=True)
    st.checkbox("Bill of Lading (B/L)", value=True, disabled=True)
    st.checkbox("Commercial Invoice", value=True, disabled=True)
    st.checkbox("Packing List (PL)", value=True, disabled=True)
    
    st.markdown("---")
    st.caption("v1.2.0 | Built by hck717")

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
            p = prompt.lower()
            if "why" in p and "compliant" in p:
                response = f"The transaction is compliant because: {state['reasoning']}"
            elif "b/l" in p or "bill of lading" in p:
                res = next((r for r in state['validation_results'] if r['doc'] == 'B/L'), None)
                if res:
                    response = f"The B/L was checked for {res['check']}. Result: {res['reason']}"
            elif "weight" in p:
                 res = next((r for r in state['validation_results'] if 'Weight' in r['check']), None)
                 if res:
                     response = f"I checked the Gross Weight between Packing List and B/L. {res['reason']}"
            else:
                response = "I can explain the compliance verdict, specific document checks (B/L, Invoice, PL), or discrepancy reasons. What would you like to know?"
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
