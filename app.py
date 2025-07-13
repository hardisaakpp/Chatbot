import json

from flask import Flask, render_template, request, jsonify

from preprocessing import preprocess

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chatbot_response():
    try:
        user_input = request.form['user_input'].strip().lower()
        response = get_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)