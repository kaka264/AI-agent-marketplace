from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt, datetime, requests, os

app = Flask(__name__)
CORS(app)

SECRET = "CHANGE_THIS_SECRET"
API_KEY = os.getenv("OPENROUTER_API_KEY")

users = []
payments = []

agents = [
    {"id": 1, "name": "Content Generator", "premium": False},
    {"id": 2, "name": "Business Chatbot", "premium": True}
]

# 🔐 Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    users.append(data)
    return jsonify({"message": "User created"})


# 🔐 Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    for u in users:
        if u["email"] == data["email"] and u["password"] == data["password"]:
            token = jwt.encode({
                "email": u["email"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }, SECRET, algorithm="HS256")

            return jsonify({"token": token})

    return jsonify({"message": "Invalid login"}), 401


# 📦 Agents
@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify(agents)


# 💰 Fake payment (replace later)
@app.route('/pay', methods=['POST'])
def pay():
    email = request.json["email"]
    payments.append(email)
    return jsonify({"message": "Premium unlocked"})


# 🤖 Run agent
@app.route('/run-agent', methods=['POST'])
def run_agent():
    token = request.headers.get("Authorization")

    try:
        user = jwt.decode(token, SECRET, algorithms=["HS256"])
        email = user["email"]
    except:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    agent = next(a for a in agents if a["id"] == data["agent_id"])

    if agent["premium"] and email not in payments:
        return jsonify({"message": "Upgrade required"}), 403

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": data["prompt"]}]
        }
    )

    return jsonify({
        "result": response.json()["choices"][0]["message"]["content"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)