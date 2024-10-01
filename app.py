from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess

# Initialize Flask app, setting the static_folder to the current directory
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS

@app.route('/')
def home():
    # Serve index.html from the main directory
    return app.send_static_file('index.html')

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
            # Filter out unnecessary console messages
            filtered_response = '\n'.join([line for line in response.splitlines() if "failed to get console mode" not in line])
            return jsonify({'reply': filtered_response})
        else:
            return jsonify({'reply': 'Error occurred: ' + error.decode('utf-8')})

    return jsonify({'reply': 'I didn’t understand that. Could you please rephrase?'})

if __name__ == '__main__':
    app.run(debug=True)
