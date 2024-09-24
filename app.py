from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(_name_)
CORS(app)  # Add this line to enable CORS

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message')

    if user_message:
        process = subprocess.Popen([r'C:\Users\pawel\AppData\Local\Programs\Ollama\ollama.exe', 'run', 'llama2:7b', user_message],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if output:
            response = output.decode('utf-8')
            filtered_response = '\n'.join([line for line in response.splitlines() if "failed to get console mode" not in line])
            return jsonify({'reply': filtered_response})
        else:
            return jsonify({'reply': 'Error occurred: ' + error.decode('utf-8')})

    return jsonify({'reply': 'I didn’t understand that. Could you please rephrase?'})

if _name_ == '_main_':
    app.run(debug=True)