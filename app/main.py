from app.agents.graph import build_graph

def run_demo():
    print("🚀 Starting Trade Finance Agent System (POC)...")
    print("==================================================")
    
    # Initialize the Graph
    app = build_graph()
    
    # Run the Workflow
    # The 'planner' node initializes the state, so we pass an empty dict initially
    final_state = app.invoke({})
    
    print("\n==================================================")
    print("🏁 FINAL VERDICT:", final_state["final_verdict"])
    print("📝 REASONING:", final_state["reasoning"])
    print("==================================================")
    
    print("\n🔍 Detailed Validation Results:")
    for res in final_state["validation_results"]:
        status_icon = "✅" if res["status"] == "Compliant" else "❌"
        print(f"{status_icon} [{res['doc']}] {res['check']}: {res['reason']}")

if __name__ == "__main__":
    run_demo()
