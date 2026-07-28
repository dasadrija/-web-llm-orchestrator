import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def interactive_wrapper_builder():
    console.print("[bold cyan]=== Interactive LLM Website Wrapper Generator ===[/bold cyan]")
    
    persona = Prompt.ask("Enter system persona/instructions for your website bot", default="You are a helpful customer support agent.")
    model_choice = Prompt.ask("Choose LLM model", choices=["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], default="gpt-4o")
    output_filename = Prompt.ask("Enter output filename for the generated website backend script", default="generated_api.py")

    code_template = f'''# Auto-generated LLM Wrapper Script for Website Integration
from flask import Flask, request, jsonify
from src.wrapper import ProductionLLMWrapper

app = Flask(__name__)
llm = ProductionLLMWrapper(model="{model_choice}", system_prompt="{persona}")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({{"error": "Message is required"}}), 400
    
    response_text = llm.query(user_message)
    return jsonify({{"response": response_text}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
'''

    with open(output_filename, "w") as f:
        f.write(code_template)
    
    console.print(f"[bold green]Success! Generated custom website backend saved to: {output_filename}[/bold green]")

if __name__ == "__main__":
    interactive_wrapper_builder()
