import gradio as gr
import os
import requests
import json

# 🧩 STEP 1: Read Groq API key from environment (Render me set karenge)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if key exists
if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY not found. Set it in Render Environment Variables.")

# 🧩 STEP 2: Ask Groq function
def ask_groq(prompt, model="llama-3.1-8b-instant"):  # ✅ Updated model name
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are Adarsh GPT, a helpful AI assistant created by Adarsh."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, data=json.dumps(data))
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
        return reply.strip()
    except requests.exceptions.HTTPError as http_err:
        return f"⚠️ HTTP error: {http_err}\nResponse: {res.text}"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# 🧩 STEP 3: Chat function
def chat_fn(message, chat_history):
    bot_reply = ask_groq(message)
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": bot_reply})
    print(f"[User]: {message}")
    print(f"[Bot]: {bot_reply}\n")
    return chat_history, chat_history

# 🧩 STEP 4: UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align:center;'>🤖 Adarsh GPT </h1>")
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(placeholder="Type your message here...")
    state = gr.State([])
    msg.submit(chat_fn, inputs=[msg, state], outputs=[chatbot, state])
    gr.Button("Clear").click(lambda: [], outputs=[chatbot])

# 🧩 STEP 5: Launch app (Render automatically sets host/port)
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 10000)),
        share=False
    )

