import gradio as gr
import os
import json
import ollama

# 🔹 Initialize Ollama client
client = ollama

# 🔹 File to persist chat history
HISTORY_FILE = "chat_history.json"

# 🔹 Load chat history if exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        chat_history_storage = json.load(f)
else:
    chat_history_storage = []

# 🔹 Function to call Ollama local model
def ask_ollama(prompt, chat_history=[], model="llama3.1"):
    messages = []
    for user_msg, bot_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    # Add latest message
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat(model=model, messages=messages)
        # ✅ Ollama API returns content inside `response["message"]["content"]`
        return response["message"]["content"].strip()
    except Exception as e:
        return f"[Error]: {str(e)}"

# 🔹 Chat function for Gradio
def chat_fn(message, chat_history, model):
    bot_reply = ask_ollama(message, chat_history, model=model)

    # Update internal history
    chat_history.append((message, bot_reply))
    chat_history_storage.append((message, bot_reply))

    # Save to persistent storage
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history_storage, f, ensure_ascii=False, indent=2)

    # Convert to Gradio Chatbot format
    gr_chat_history = []
    for user_msg, bot_msg in chat_history:
        gr_chat_history.append({"role": "user", "content": user_msg})
        gr_chat_history.append({"role": "assistant", "content": bot_msg})

    return gr_chat_history, chat_history

# 🔹 Clear chat function
def clear_chat():
    chat_history_storage.clear()
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return []

# 🔹 Model to use
model_select = "llama3.1"  # Change to "mistral" if you want

# 🔹 Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align:center;'>🤖 Adarsh GPT</h1>")
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(placeholder="Type your message here...")
    state = gr.State(chat_history_storage)

    # Submit message
    msg.submit(chat_fn, inputs=[msg, state, gr.State(model_select)], outputs=[chatbot, state])

    # Clear button
    gr.Button("Clear Chat").click(clear_chat, outputs=[chatbot])

# 🔹 Launch for Render hosting
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
