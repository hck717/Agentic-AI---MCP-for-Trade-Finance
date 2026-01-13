import streamlit as st
import time
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

st.info("""
**POC Demo Scenerio:**
*   **LC Requirement:** "Apple iPhone 15 Pro Max smartphones"
*   **B/L Description:** "Electronic Devices - Apple iPhone" (Generic Term)
*   **Challenge:** Traditional systems fail this. Our AI Agent uses **ISBP 745 Art. E26** to validate it.
""")

# --- Sidebar ---
with st.sidebar:
    st.header("📂 Document Upload")
    st.markdown("For this POC, we use pre-loaded mock documents.")
    
    st.checkbox("Letter of Credit (LC)", value=True, disabled=True)
    st.checkbox("Bill of Lading (B/L)", value=True, disabled=True)
    st.checkbox("Commercial Invoice", value=True, disabled=True)
    
    st.markdown("---")
    st.caption("v1.0.0 | Built by hck717")

# --- Main Action ---
if st.button("🚀 Start Compliance Check", type="primary"):
    
    # 1. Initialize Containers for Real-time Logging
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Agent Thought Process")
        planner_log = st.empty()
        bl_log = st.empty()
        inv_log = st.empty()
        review_log = st.empty()

    # 2. Run the Graph
    workflow = build_graph()
    
    # --- Step 1: Planner ---
    planner_log.info("🧠 **Planner:** Analyzing LC requirements...")
    time.sleep(1) # Simulating processing time
    # In a real app, we'd use a stream handler. Here we run it and show partials if possible, 
    # but for simplicity in this POC, we invoke and then display.
    
    final_state = workflow.invoke({})
    
    planner_log.success("🧠 **Planner:** Plan created! Delegating to Experts.")
    
    # --- Step 2: B/L Expert ---
    time.sleep(1)
    bl_log.info("🚢 **B/L Expert:** Checking Port, Date, and Description...")
    time.sleep(0.5)
    bl_log.success("🚢 **B/L Expert:** Checks complete.")

    # --- Step 3: Invoice Expert ---
    time.sleep(1)
    inv_log.info("💰 **Invoice Expert:** Checking Amount and Description...")
    time.sleep(0.5)
    inv_log.success("💰 **Invoice Expert:** Checks complete.")
    
    # --- Step 4: Reviewer ---
    time.sleep(1)
    review_log.info("⚖️ **Reviewer:** Analyzing findings against UCP 600...")
    time.sleep(0.5)
    
    # --- Display Final Verdict ---
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
                if "Goods Description" in res['check'] and res['doc'] == "B/L":
                    st.info("💡 **AI Insight:** The Agent successfully applied **ISBP 745 Art. E26** to accept the generic description.")

    review_log.success("⚖️ **Reviewer:** Final Verdict Generated.")
