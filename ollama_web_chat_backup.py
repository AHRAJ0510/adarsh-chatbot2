import gradio as gr
import requests
import json
from datetime import datetime

# 🔹 Function to log chats in a file
def log_chat(user_input, bot_reply):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] User: {user_input}\n")
        f.write(f"[{time}] Bot: {bot_reply}\n")
        f.write("="*50 + "\n")

# 🔹 Function to ask Ollama
def ask_ollama(prompt, model="gpt-oss:120b-cloud"):
    url = "http://localhost:11434/api/generate"
    data = {"model": model, "prompt": prompt}
    reply = ""
    try:
        response = requests.post(url, json=data, stream=True)
        for line in response.iter_lines():
            if line:
                try:
                    data_line = json.loads(line.decode("utf-8"))
                    if "response" in data_line:
                        reply += data_line["response"]
                except json.JSONDecodeError:
                    continue
        return reply
    except Exception as e:
        return f"[Error]: {e}"

# 🔹 Chat function for Gradio
def chat_fn(message, chat_history):
    bot_reply = ask_ollama(message, model=model_select)
    chat_history.append((message, bot_reply))
    
    # 🟢 Log the chat in text file
    log_chat(message, bot_reply)
    
    return chat_history, chat_history

# 🔹 Choose model
model_select = "gpt-oss:120b-cloud"  # cloud
# model_select = "mistral:latest"    # local

# 🔹 Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align:center;'>🤖 Adarsh GPT </h1>")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message here...")
    state = gr.State([])

    msg.submit(chat_fn, inputs=[msg, state], outputs=[chatbot, state])
    gr.Button("Clear").click(lambda: [], outputs=[chatbot])

demo.launch(share=True)
