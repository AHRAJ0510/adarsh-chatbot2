import gradio as gr
import requests

# 🔹 Ollama local API
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-oss:120b-cloud"

def chat_with_ollama(message, history):
    """Send message to Ollama and return the response text."""
    try:
        payload = {
            "model": MODEL,
            "prompt": message,
            "stream": False
        }
        res = requests.post(OLLAMA_URL, json=payload)
        data = res.json()
        return data.get("response", "❌ No response received from model.")
    except Exception as e:
        return f"[Error]: {str(e)}"

def respond(message, history):
    """Handle text message input."""
    if history is None:
        history = []
    # add user message in OpenAI-style format
    history.append({"role": "user", "content": message})
    reply = chat_with_ollama(message, history)
    history.append({"role": "assistant", "content": reply})
    return history, ""

with gr.Blocks(title="Adarsh Web Chatbot") as demo:
    gr.Markdown("## 🤖 Adarsh Web Chatbot (Powered by Ollama GPT Cloud)")
    
    # ✅ type='messages' for new Gradio versions
    chatbot = gr.Chatbot(label="Adarsh Chatbot", type="messages")

    msg = gr.Textbox(
        label="Type your message below or use mic 🎤",
        placeholder="Say something or type here..."
    )
    
    # ✅ Correct mic param (plural)
    mic = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak")

    with gr.Row():
        send_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear Chat")

    # Button events
    send_btn.click(respond, [msg, chatbot], [chatbot, msg])
    clear_btn.click(lambda: [], None, chatbot)

    # Mic event (just simulates voice message acknowledgment)
    def process_voice(audio_path, history):
        if not audio_path:
            return history, ""
        message = "🎙️ (Voice message sent)"
        history.append({"role": "user", "content": message})
        reply = chat_with_ollama("User sent a voice message.", history)
        history.append({"role": "assistant", "content": reply})
        return history, ""
    
    mic.change(process_voice, [mic, chatbot], [chatbot, msg])

if __name__ == "__main__":
    demo.launch()
