# --- Chat Interface ---
st.markdown("---")
st.subheader("💬 AI Compliance Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the compliance check..."):
    # Add user message
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
            
            # --- IMPROVED LOGIC START ---
            
            # 1. Check for specific document failures (e.g. "invoice failed", "why invoice")
            if "invoice" in p and ("fail" in p or "discrep" in p or "wrong" in p or "why" in p):
                # Find the invoice result
                res = next((r for r in state['validation_results'] if r['doc'] == 'Invoice'), None)
                if res:
                    status_icon = "✅" if res['status'] == 'Compliant' else "❌"
                    response = f"**Invoice Check ({status_icon} {res['status']}):** {res['reason']}"
                else:
                    response = "I couldn't find a specific check result for the Invoice."

            # 2. Check for B/L failures
            elif ("b/l" in p or "bill of lading" in p) and ("fail" in p or "discrep" in p or "wrong" in p or "why" in p):
                res = next((r for r in state['validation_results'] if r['doc'] == 'B/L' and 'Description' in r['check']), None)
                 # If looking for description specifically
                if res:
                    status_icon = "✅" if res['status'] == 'Compliant' else "❌"
                    response = f"**B/L Check ({status_icon} {res['status']}):** {res['reason']}"
                else:
                    # Fallback to any B/L check
                    res = next((r for r in state['validation_results'] if r['doc'] == 'B/L'), None)
                    if res:
                         response = f"**B/L Check:** {res['reason']}"

            # 3. Check for PL / Weight failures
            elif ("packing list" in p or "pl" in p or "weight" in p) and ("fail" in p or "discrep" in p or "wrong" in p or "why" in p):
                 res = next((r for r in state['validation_results'] if r['doc'] == 'PackingList'), None)
                 if res:
                    status_icon = "✅" if res['status'] == 'Compliant' else "❌"
                    response = f"**Packing List Check ({status_icon} {res['status']}):** {res['reason']}"

            # 4. General "Why" or "Verdict"
            elif "compliant" in p or "verdict" in p or "result" in p:
                response = f"**Final Verdict:** {state['final_verdict']}\n\n**Reasoning:** {state['reasoning']}"
            
            # 5. Fallback for "Why" without specific context (Try to find ANY discrepancy)
            elif "why" in p:
                 discrepancies = [r for r in state['validation_results'] if r['status'] == 'Discrepant']
                 if discrepancies:
                     reasons = "\n".join([f"- **{d['doc']} {d['check']}:** {d['reason']}" for d in discrepancies])
                     response = f"The following discrepancies were found:\n{reasons}"
                 else:
                     response = "Everything looks compliant! All checks passed."

            # 6. Generic Fallback
            else:
                response = "I can explain the compliance verdict. Try asking: \n- 'Why did the Invoice fail?'\n- 'Why is the B/L compliant?'\n- 'Show me the discrepancies.'"
            
            # --- IMPROVED LOGIC END ---

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
