import os
import sys

# Add src to python path if not already there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from graph import app_graph

def main():
    print("🤖 Agentic Commerce CLI 🤖")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue
                
            initial_state = {
                "user_query": user_input,
                "analysis": "",
                "response": ""
            }
            
            print("Thinking...")
            # Invoke LangGraph
            final_state = app_graph.invoke(initial_state)
            
            # Retrieve results
            response_text = final_state.get("response", "No response generated.")
            print(f"\nAgent: {response_text}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    main()
