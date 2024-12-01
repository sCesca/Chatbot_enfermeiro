from chatterbot import ChatBot 
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("EnfermeiroBot")

trainer = ListTrainer(chatbot)
conversation = [
    "Olá, como posso ajudar?",
    "Quais são os sintomas?",
    "Se os sintomas persistirem, procure por um médico!"
]
trainer.train(conversation)

def get_response(message):
    response = chatbot.get_response(message)
    return str(response)