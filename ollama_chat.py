import requests

def ask_ollama(prompt, model="mistral:latest"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt
    }

    response = requests.post(url, json=data, stream=True)
    full_reply = ""
    for line in response.iter_lines():
        if line:
            part = line.decode('utf-8')
            if '"response":"' in part:
                text = part.split('"response":"')[1].split('"')[0]
                full_reply += text
    return full_reply

print("🤖 Local AI Chatbot (Ollama + Mistral)")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye 👋")
        break
    reply = ask_ollama(user_input, model="gpt-oss:120b-cloud")

    print("Bot:", reply)
