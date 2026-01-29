from agent.chat_agent import ChatAgent
from config import CSV_PATH

def main():
    print("\n" + "="*60)
    print("CSV Data Agent - Terminal Mode")
    print("="*60)
    print("Commands: 'exit' or 'quit' to exit, 'clear' to reset\n")
    
    agent = ChatAgent(CSV_PATH)
    history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye\n")
                break
            
            if user_input.lower() == 'clear':
                history = []
                print("\nHistory cleared!\n")
                continue
            
            if not user_input:
                continue
            
            response = agent.process_message_sync(user_input, history)
            
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            print(f"\n Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n\n Goodbye!\n")
            break
        except Exception as e:
            print(f"\n  Error: {e}\n")

if __name__ == "__main__":
    main()
