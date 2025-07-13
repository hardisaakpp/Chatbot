import json
from preprocessing import preprocess
import tkinter as tk
from tkinter import scrolledtext

# Load predefined responses
with open('responses.json', 'r', encoding='utf-8') as file:
    responses = json.load(file)

def get_response(user_input):
    tokens = preprocess(user_input)
    for question, answer in responses['preguntas_frecuentes'].items():
        question_tokens = preprocess(question)
        if set(tokens).intersection(set(question_tokens)):
            return answer
    return "Lo siento, no tengo una respuesta para esa pregunta."

def send_message():
    user_input = user_entry.get()
    if user_input.lower() in ["salir", "adiós"]:
        root.quit()
    else:
        response = get_response(user_input)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Tú: " + user_input + "\n")
        chat_area.insert(tk.END, "Chatbot: " + response + "\n\n")
        chat_area.config(state=tk.DISABLED)
        user_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Chatbot de Asistencia Académica")

# Create the chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create the text entry box
user_entry = tk.Entry(root, width=100)
user_entry.pack(padx=10, pady=10, fill=tk.X)
user_entry.bind("<Return>", lambda event: send_message())

# Create the send button
send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(padx=10, pady=10)

# Start the main loop
root.mainloop()