import gradio as gr
import requests
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # voice speed

# Function to set voice properties
def set_voice_settings(gender, language):
    voices = engine.getProperty('voices')
    selected_voice = None

    for voice in voices:
        if gender.lower() in voice.name.lower() and language.lower() in voice.name.lower():
            selected_voice = voice
            break

    # fallback to default voice
    if not selected_voice:
        selected_voice = voices[0]
    engine.setProperty('voice', selected_voice.id)

# Chat function
def chat_with_ollama(message, history, gender, language):
    """Send message to Ollama and get response"""
    set_voice_settings(gender, language)
    model = "mistral"  # change if using another model
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": model, "prompt": message}

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    content = line.decode("utf-8").split('"response":"')[1].split('"')[0]
                    response_text += content
                except:
                    pass

        # Speak the response
        if language.lower() == "hindi":
            engine.say(response_text)
        else:
            engine.say(response_text)
        engine.runAndWait()

        # Update chat history (Gradio format)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response_text})
        return history
    except Exception as e:
        return [{"role": "assistant", "content": f"Error: {str(e)}"}]

# UI
with gr.Blocks(title="Adarsh Voice Chatbot") as demo:
    gr.Markdown("## 🎙️ Adarsh Voice Chatbot — Text Input + Voice Output (with Voice & Language Control)")
    chatbot = gr.Chatbot(label="Adarsh Chatbot", type="messages")
    msg = gr.Textbox(label="💬 Enter your message")
    gender = gr.Radio(["Male", "Female"], value="Male", label="🧑‍🦱 Select Voice Gender")
    language = gr.Radio(["English", "Hindi"], value="English", label="🌐 Select Language")

    msg.submit(chat_with_ollama, [msg, chatbot, gender, language], [chatbot])

demo.launch()
