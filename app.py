from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from agent.chat_agent import ChatAgent
from config import CSV_PATH
import os
import time

app = FastAPI(title="CSV Data Agent")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ChatAgent(CSV_PATH)
chat_sessions = {}

class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]

class ClearRequest(BaseModel):
    session_id: str = "default"

@app.get("/", response_class=HTMLResponse)
async def root():
    # Add timestamp to bust cache
    ts = str(int(time.time()))
    return HTMLResponse(content=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>CSV Data Agent - v{ts}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }}
        .container {{ background: white; border-radius: 24px; box-shadow: 0 24px 48px rgba(0,0,0,0.2); width: 100%; max-width: 900px; height: 700px; display: flex; flex-direction: column; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px 28px; border-radius: 24px 24px 0 0; display: flex; align-items: center; gap: 16px; }}
        .logo {{ width: 48px; height: 48px; background: rgba(255,255,255,0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; }}
        .header-text h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 4px; }}
        .header-text p {{ font-size: 14px; opacity: 0.9; }}
        .chat-container {{ flex: 1; overflow-y: auto; padding: 24px; background: #f8fafc; }}
        .message {{ margin-bottom: 16px; display: flex; gap: 12px; }}
        .message.user {{ justify-content: flex-end; }}
        .avatar {{ width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 18px; }}
        .message.user .avatar {{ background: linear-gradient(135deg, #667eea, #764ba2); order: 2; }}
        .message.assistant .avatar {{ background: linear-gradient(135deg, #10b981, #059669); }}
        .message-content {{ max-width: 65%; padding: 14px 18px; border-radius: 16px; line-height: 1.6; white-space: pre-wrap; }}
        .message.user .message-content {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-bottom-right-radius: 4px; }}
        .message.assistant .message-content {{ background: white; color: #334155; border: 1px solid #e2e8f0; border-bottom-left-radius: 4px; }}
        .input-area {{ padding: 20px 24px; background: white; border-top: 1px solid #e2e8f0; border-radius: 0 0 24px 24px; }}
        .loading {{ display: none; align-items: center; gap: 8px; padding: 10px 16px; background: #eff6ff; border: 1px solid #dbeafe; border-radius: 12px; color: #1e40af; font-size: 14px; margin-bottom: 12px; }}
        .loading.active {{ display: flex; }}
        .spinner {{ width: 16px; height: 16px; border: 2px solid #dbeafe; border-top-color: #3b82f6; border-radius: 50%; animation: spin 0.8s linear infinite; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        .input-wrapper {{ display: flex; gap: 12px; background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 16px; padding: 8px; }}
        .input-wrapper:focus-within {{ background: white; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.1); }}
        input {{ flex: 1; padding: 10px 12px; border: none; background: transparent; font-size: 15px; outline: none; }}
        button {{ padding: 12px 24px; border: none; border-radius: 12px; cursor: pointer; font-weight: 600; font-size: 14px; }}
        button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .btn-send {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .btn-clear {{ background: #ef4444; color: white; }}
        .welcome {{ background: linear-gradient(135deg, #eff6ff, #dbeafe); border: 1px solid #bfdbfe; border-radius: 16px; padding: 20px; }}
        .welcome h3 {{ color: #1e40af; font-size: 16px; margin-bottom: 12px; }}
        .welcome ul {{ list-style: none; padding: 0; }}
        .welcome li {{ padding: 6px 0; color: #1e3a8a; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📊</div>
            <div class="header-text">
                <h1>CSV Data Agent</h1>
                <p>AI-Powered Data Analytics</p>
            </div>
        </div>
        <div class="chat-container" id="chat"></div>
        <div class="input-area">
            <div class="loading" id="load"><div class="spinner"></div><span>Processing...</span></div>
            <div class="input-wrapper">
                <button class="btn-clear" id="clr">🗑️ Clear</button>
                <input type="text" id="inp" placeholder="Ask me anything...">
                <button class="btn-send" id="snd">Send →</button>
            </div>
        </div>
    </div>
    <script>
        console.log('v{ts}');
        var chat=document.getElementById('chat');
        var inp=document.getElementById('inp');
        var snd=document.getElementById('snd');
        var clr=document.getElementById('clr');
        var load=document.getElementById('load');
        
        chat.innerHTML='<div class="welcome"><h3>👋 Welcome!</h3><ul><li>→ What columns?</li><li>→ Show overview</li><li>→ Calculate stats</li></ul></div>';
        
        function add(txt,role){{
            var m=document.createElement('div');
            m.className='message '+role;
            var a=document.createElement('div');
            a.className='avatar';
            a.textContent=role==='user'?'👤':'🤖';
            var c=document.createElement('div');
            c.className='message-content';
            c.textContent=txt;
            m.appendChild(a);
            m.appendChild(c);
            chat.appendChild(m);
            chat.scrollTop=chat.scrollHeight;
        }}
        
        function send(){{
            var msg=inp.value.trim();
            if(!msg)return;
            console.log('Sending:',msg);
            add(msg,'user');
            inp.value='';
            snd.disabled=true;
            load.classList.add('active');
            fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:msg,session_id:'default'}})}})
            .then(function(r){{return r.json();}})
            .then(function(d){{add(d.response,'assistant');}})
            .catch(function(e){{add('Error: '+e.message,'assistant');}})
            .finally(function(){{snd.disabled=false;load.classList.remove('active');inp.focus();}});
        }}
        
        function clear(){{
            if(!confirm('Clear?'))return;
            fetch('/clear',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{session_id:'default'}})}})
            .then(function(){{chat.innerHTML='<div class="welcome"><h3>✨ Cleared!</h3></div>';}});
        }}
        
        snd.onclick=send;
        clr.onclick=clear;
        inp.onkeypress=function(e){{if(e.key==='Enter')send();}};
        
        fetch('/health').then(function(r){{return r.json();}}).then(function(d){{console.log('OK:',d);}});
        inp.focus();
        console.log('Ready!');
    </script>
</body>
</html>
    """)

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        print(f"\n📨 {message.message[:50]}")
        if not message.message.strip():
            raise HTTPException(status_code=400, detail="Empty")
        if message.session_id not in chat_sessions:
            chat_sessions[message.session_id] = []
        history = chat_sessions[message.session_id]
        response = agent.process_message_sync(message.message, history)
        history.append({"role": "user", "content": message.message})
        history.append({"role": "assistant", "content": response})
        print(f"✅ Sent\n")
        return ChatResponse(response=response, history=history)
    except Exception as e:
        print(f"❌ {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_chat(request: ClearRequest):
    try:
        print(f"\n🗑️ {request.session_id}")
        if request.session_id in chat_sessions:
            chat_sessions[request.session_id] = []
        print("✅ Cleared\n")
        return {"status": "cleared"}
    except Exception as e:
        print(f"❌ {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model": agent.model}