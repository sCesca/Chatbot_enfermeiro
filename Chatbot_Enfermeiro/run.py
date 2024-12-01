import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Possíveis respostas do usuário
symptoms_database = {
    "febre": "moderada",
    "dor no peito": "grave",
    "dor no peito ao respirar": "grave",
    "dor de cabeça": "leve",
    "tosse": "leve",
    "tosse seca": "leve",
    "tosse com catarro": "moderada",
    "falta de ar": "grave",
    "dificuldade para respirar": "grave",
    "dor nas costas": "moderada",
    "dores musculares": "leve",
    "dor abdominal": "moderada",
    "enjoo": "leve",
    "vômito": "moderada",
    "diarreia": "moderada",
    "calafrios": "moderada",
    "tontura": "moderada",
    "cansaço excessivo": "moderada",
    "fraqueza": "moderada",
    "manchas na pele": "moderada",
    "coceira": "leve",
    "erupções cutâneas": "moderada",
    "sangramento nasal": "moderada",
    "dor na garganta": "leve",
    "dor de ouvido": "moderada",
    "perda de apetite": "leve",
    "confusão mental": "grave",
    "desmaio": "grave",
    "visão turva": "moderada",
    "palpitações": "grave",
    "inchaço nas pernas": "moderada",
    "inchaço no rosto": "grave",
    "sede excessiva": "moderada",
    "dor ao urinar": "moderada",
    "sangue na urina": "grave",
    "queda de cabelo": "leve",
    "febre alta": "grave",
    "tremores": "moderada",
    "perda de olfato": "moderada",
    "perda de paladar": "moderada"
}

def evaluate_symptoms(user_message):
    response = "Desculpe, não entendi sua pergunta."
    for symptom, severity in symptoms_database.items():
        if symptom in user_message.lower():
            response = f"Você mencionou o sintoma: {symptom}. Classificação: {severity}."
            if severity == "grave":
                response += " Recomendo que procure um médico imediatamente."
            elif severity == "leve":
                response += " Você pode ficar de repouso."
            else:
                response += " Não encontrei esse sintoma na minha base de dados, recomendo que procure um médico."
            break

    save_message(user_message, response)
    return response

def save_message(user_message, bot_response):
    db_path = os.path.expanduser('~/Desktop/Chatbot_Enfermeiro/Chatbot_Enfermeiro/chatbot-enfermeiro/messages.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO messages (user_message, bot_response)
    VALUES (?, ?)
    ''', (user_message, bot_response))

    conn.commit()
    conn.close()

def get_messages_history():
    db_path = os.path.expanduser('~/Desktop/Chatbot_Enfermeiro/Chatbot_Enfermeiro/chatbot-enfermeiro/messages.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT user_message, bot_response
    FROM messages
    ORDER BY rowid DESC
    ''')

    messages = cursor.fetchall()
    conn.close()

    return messages


@app.route('/')
def home():
    return "Bem-vindo à API Flask! Vá para /chatbot para conversar com o chatbot."

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            response = evaluate_symptoms(user_message)
    
    messages = get_messages_history()

    return render_template_string('''
        <html>
        <head>
            <title>Chatbot Enfermeiro</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .chat-container { max-width: 600px; margin: auto; }
                .chat-box { border: 1px solid #ccc; padding: 10px; border-radius: 5px; max-height: 400px; overflow-y: auto; }
                .user-message { color: blue; }
                .bot-response { color: green; }
                .message { margin: 10px 0; }
                .input-container { display: flex; margin-top: 10px; }
                .input-container input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
                .input-container button { padding: 10px; border: none; background-color: #28a745; color: white; border-radius: 5px; margin-left: 10px; cursor: pointer; }
                .input-container button:hover { background-color: #218838; }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <h2>Chatbot Enfermeiro</h2>
                <div id="chat-box" class="chat-box">
                    {% for user_message, bot_response in messages %}
                        <div class="message user-message">Você: {{ user_message }}</div>
                        <div class="message bot-response">Chatbot: {{ bot_response }}</div>
                    {% endfor %}
                </div>
                <form method="POST" class="input-container">
                    <input type="text" id="message" name="message" placeholder="Escreva sua mensagem para o chatbot">
                    <button type="submit">Enviar</button>
                </form>
            </div>
        </body>
        </html>
    ''', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
