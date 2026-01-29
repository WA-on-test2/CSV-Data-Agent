import json
from typing import List, Dict
from openai import OpenAI
from tools.csv_tools import CSVTools
from config import API_KEY, BASE_URL, MODEL, SYSTEM_PROMPT

class ChatAgent:
    def __init__(self, csv_path: str):
        self.client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        self.tools_handler = CSVTools(csv_path)
        self.tool_definitions = self._get_tool_definitions()
        self.model = MODEL
    
    def _get_tool_definitions(self) -> List[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_columns",
                    "description": "List all columns in the CSV",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "dataset_overview",
                    "description": "Get dataset size and structure",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "average",
                    "description": "Compute average of a numeric column",
                    "parameters": {
                        "type": "object",
                        "properties": {"column": {"type": "string"}},
                        "required": ["column"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "group_average",
                    "description": "Average a numeric column grouped by another column",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "group_by": {"type": "string"},
                            "target": {"type": "string"}
                        },
                        "required": ["group_by", "target"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "filter_rows",
                    "description": "Filter rows using numeric condition",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "column": {"type": "string"},
                            "operator": {"type": "string", "enum": [">", "<", "=="]},
                            "value": {"type": "number"}
                        },
                        "required": ["column", "operator", "value"]
                    }
                }
            }
        ]
    
    def process_message_sync(self, user_input: str, history: List[Dict]) -> str:
        """Synchronous message processing for FastAPI"""
        print("=" * 60)
        print(f"USER: {user_input}")
        print("=" * 60)
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Restore conversation history
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        
        messages.append({"role": "user", "content": user_input})
        
        # Initial API call
        print("Calling LLM...\n")
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self.tool_definitions
        )
        
        msg = response.choices[0].message
        messages.append(msg.model_dump())
        
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            
            result = self.tools_handler.execute_tool(
                tool_call.function.name, 
                args
            )
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
            
            messages.append({
                "role": "user",
                "content": (
                    "Explain the result in **Markdown**.\n"
                    "- Use bullet points\n"
                    "- Give insights\n"
                    "- Do NOT show JSON"
                )
            })
            
            print("Generating formatted response...\n")
            final = self.client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            
            answer = final.choices[0].message.content
        else:
            answer = msg.content
        
        print(f"RESPONSE: {answer[:100]}...\n")
        print("=" * 60 + "\n")
        
        return answer