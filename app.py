from flask import Flask, render_template_string, request, jsonify
from src.wrapper import ProductionLLMWrapper

app = Flask(__name__)
llm = ProductionLLMWrapper()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LLM Website Assistant</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 420px; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .chat-box { height: 350px; border: 1px solid #e4e6eb; border-radius: 8px; overflow-y: scroll; padding: 12px; margin-bottom: 15px; display: flex; flex-direction: column; gap: 10px; background: #fafafa; }
        .message { padding: 10px 14px; border-radius: 8px; max-width: 80%; line-height: 1.4; word-wrap: break-word; }
        .user { background: #0084ff; color: white; align-self: flex-end; }
        .bot { background: #e4e6eb; color: #050505; align-self: flex-start; }
        .input-group { display: flex; gap: 8px; }
        input { flex: 1; padding: 10px; border: 1px solid #ccd0d5; border-radius: 6px; outline: none; font-size: 14px; }
        input:focus { border-color: #0084ff; }
        button { padding: 10px 18px; background: #0084ff; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #006edd; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h3>Website AI Assistant</h3>
        <div class="chat-box" id="chatBox"></div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="Ask something..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = input.value.trim();
            if(!text) return;
            
            chatBox.innerHTML += `<div class="message user">${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
            
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chatBox.innerHTML += `<div class="message bot">${data.response}</div>`;
            } catch (err) {
                chatBox.innerHTML += `<div class="message bot">Error connecting to server.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    reply = llm.query(user_msg)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
