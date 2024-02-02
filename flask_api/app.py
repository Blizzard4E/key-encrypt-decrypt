from flask import Flask, jsonify, request
from flask_cors import CORS

from security_utils import decrypt_text, encrypt_text

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return jsonify(message='Hello, World!')

@app.route('/text', methods=['POST'])
def encrypt_text_route():
    print(request.get_data()) 
    # Check if request has JSON data
    if not request.is_json:
        return jsonify(error='Invalid JSON data'), 400

    # Get the 'original_text' from the request JSON
    data = request.get_json()
    original_text = data.get('original_text')
    key = data.get('key') 

    # Check if 'original_text' is provided
    if not original_text:
        return jsonify(error='Missing original_text'), 400

    # Call the encrypt_text function
    encrypted_text = encrypt_text(key, original_text) 
    decrypted_text = decrypt_text(key, encrypted_text) 
    # Return the encrypted text
    return jsonify(encrypted_text=encrypted_text, decrypted_text=decrypted_text) 

if __name__ == '__main__':
    app.run(debug=True)
