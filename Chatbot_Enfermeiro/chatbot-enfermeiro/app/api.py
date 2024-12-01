from flask import Flask, request, jsonify
from app.bot_logic import get_response
from app.symptoms_data import evaluate_symptoms\
from app.database import save_patient


app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json
    response = get_response(user_message)

    return jsonify({"response":response})

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    symptoms = data.get("symptoms")
    evaluation = evaluate_symptoms(symptoms)
    save_patient(name, age, symptoms, ", ".join([e["severity"] for e in evaluation]))
    return jsonify({"evaluation": evaluation})

if __name__ == "__main__":
    app.run(debug=True)