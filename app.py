from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__, static_folder=".")
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

conversation_history = []

ASTRONOMY_SYSTEM = """
You are an enthusiastic Astronomy Expert Bot! 🌌✨
You love space, stars, planets, galaxies, black holes, moons, comets, rockets and cosmic mysteries.
Rules:
- Be exciting and friendly
- Explain simply
- Use emojis naturally
- Make astronomy fun
- Give accurate answers
"""

@app.route("/")
def home():
    return send_from_directory(".", "astronomy_bot_ui.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "running"})

@app.route("/api/clear", methods=["POST"])
def clear_chat():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "cleared"})

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Empty message"}), 400

        conversation_history.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": ASTRONOMY_SYSTEM},
                *conversation_history
            ],
            max_tokens=500
        )

        reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})

        return jsonify({"response": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
