from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face Inference API setup
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_TOKEN = "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" 

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

chat_history = []

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    generated = response.json()
    return generated[0]["generated_text"]

def generate_chat(user_input):
    global chat_history
    chat_history.append(f"Patient: {user_input}")
    chat_history = chat_history[-6:]  # Keep last 3 interactions

    # Format prompt using instruction style
    prompt = (
        "[INST] You are a helpful and medically accurate assistant specialized in Chronic Kidney Disease (CKD). "
        "Respond only with medical guidance based on CKD context. \n\n"
        + "\n".join(chat_history)
        + "\nDoctor: [/INST]"
    )
    response = query_model(prompt)
    cleaned = response.strip().split("Doctor:")[-1].strip()
    chat_history.append(f"Doctor: {cleaned}")
    return cleaned

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message")
        reply = generate_chat(user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong."}), 500

if __name__ == '__main__':
    app.run(debug=True)
