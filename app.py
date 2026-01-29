from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Dict
from agent.chat_agent import ChatAgent
from config import CSV_PATH
import os

app = FastAPI(title="CSV Data Agent")
agent = ChatAgent(CSV_PATH)
chat_sessions = {}

class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_file = "static/index.html"
    if os.path.exists(html_file):
        return FileResponse(html_file)
    
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 800px;
            height: 600px;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }
        .header h1 { font-size: 24px; margin-bottom: 5px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .message.user { justify-content: flex-end; }
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .message.assistant .message-content {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
            border-radius: 0 0 20px 20px;
            display: flex;
            gap: 10px;
        }
        #messageInput {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        #messageInput:focus { border-color: #667eea; }
        button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active { transform: translateY(0); }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .clear-btn {
            background: #dc3545;
            padding: 8px 16px;
            font-size: 12px;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            padding: 10px;
            font-style: italic;
        }
        .loading.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 CSV Data Agent</h1>
            <p>Ask questions about your dataset</p>
        </div>
        <div class="chat-container" id="chatContainer"></div>
        <div class="loading" id="loading">Thinking...</div>
        <div class="input-container">
            <button class="clear-btn" onclick="clearChat()">Clear</button>
            <input type="text" id="messageInput" placeholder="Ask about the dataset..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()" id="sendBtn">Send</button>
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const loading = document.getElementById('loading');

        function addMessage(content, role) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = role === 'assistant' ? marked.parse(content) : content;
            
            messageDiv.appendChild(contentDiv);
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            messageInput.value = '';
            sendBtn.disabled = true;
            loading.classList.add('active');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, session_id: 'default' })
                });

                const data = await response.json();
                addMessage(data.response, 'assistant');
            } catch (error) {
                addMessage('Error: Could not get response', 'assistant');
            } finally {
                sendBtn.disabled = false;
                loading.classList.remove('active');
                messageInput.focus();
            }
        }

        async function clearChat() {
            if (confirm('Clear conversation history?')) {
                chatContainer.innerHTML = '';
                await fetch('/clear', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: 'default' })
                });
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') sendMessage();
        }

        // Simple markdown parser
        const marked = {
            parse: (text) => {
                return text
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.+?)\*/g, '<em>$1</em>')
                    .replace(/^- (.+)$/gm, '<li>$1</li>')
                    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
                    .replace(/\n/g, '<br>');
            }
        };

        messageInput.focus();
    </script>
</body>
</html>
    """)

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    if not message.message:
        raise HTTPException(status_code=400, detail="Empty message")
    
    # Get or create session history
    if message.session_id not in chat_sessions:
        chat_sessions[message.session_id] = []
    
    history = chat_sessions[message.session_id]
    
    # Process message
    response = agent.process_message_sync(message.message, history)
    
    # Update history
    history.append({"role": "user", "content": message.message})
    history.append({"role": "assistant", "content": response})
    
    return ChatResponse(response=response, history=history)

@app.post("/clear")
async def clear_chat(session_id: str = "default"):
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    return {"status": "cleared"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model": agent.model}
