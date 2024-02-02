import base64
from io import BytesIO 
import os
from dotenv import load_dotenv
import ssl
import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS 
import numpy as np
import cloudinary
from cloudinary.uploader import upload
import urllib.request


from security_utils import decrypt_image, decrypt_text, encrypt_image, encrypt_text
# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)
CORS(app, origins="*")

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

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@app.route('/image', methods=['POST'])
def encrypt_decrypt_original_image():
    key = request.form.get('key') 
    # Check if the request has a file part
    if 'original_image' not in request.files:
        return jsonify(error='No file part'), 400

    file = request.files['original_image']

    # Check if the file is not empty
    if file.filename == '':
        return jsonify(error='No selected file'), 400

    # Upload the original image to Cloudinary
    result = upload(file, folder="Encrypt Decrypt")

    # Get the URL of the uploaded image
    original_image_url = result['secure_url']

    #ENCRYPTION
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(original_image_url, context=context)
    image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # You can now use original_image_url as needed
    encrypted_image = encrypt_image(key, image)
     # Encode the encrypted image as base64
    _, buffer = cv2.imencode('.png', encrypted_image)
    encrypted_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Upload the encrypted image to Cloudinary
    encrypted_result = upload(BytesIO(base64.b64decode(encrypted_image_base64)),folder="Encrypt Decrypt")

    # Get the URL of the uploaded encrypted image
    encrypted_image_url = encrypted_result['secure_url'] 
    
    # DECRYPTION
    response2 = urllib.request.urlopen(encrypted_image_url, context=context)
    image_array2 = np.asarray(bytearray(response2.read()), dtype=np.uint8)
    image2 = cv2.imdecode(image_array2, cv2.IMREAD_COLOR)
    # You can now use original_image_url as needed
    decrypted_image = decrypt_image(key, image2)
     # Encode the decrypted image as base64
    _, buffer = cv2.imencode('.png', decrypted_image)
    decrypted_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Upload the decrypted image to Cloudinary
    decrypted_result = upload(BytesIO(base64.b64decode(decrypted_image_base64)), folder="Encrypt Decrypt")

    # Get the URL of the uploaded decrypted image
    decrypted_image_url = decrypted_result['secure_url']

    return jsonify(original_image_url=original_image_url,encrypted_image_url=encrypted_image_url,decrypted_image_url=decrypted_image_url), 200

if __name__ == '__main__':
    app.run(debug=True)
