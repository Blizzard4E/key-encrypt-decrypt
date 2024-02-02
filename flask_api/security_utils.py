import math
import cv2 
 
c1_value = -0.3
c2_value = 0.3
y1_value = 0.492
y2_value = -0.133

def key_func(key):
    y_array = []
    temp = [] 
    temp = ord(key[0]) + c1_value * y1_value + c2_value * y2_value 
    y_array.append(math.fmod(temp+1, 2.0) - 1) 
 
    temp = ord(key[1]) + c1_value * y_array[0] + c2_value * y1_value 
    y_array.append(math.fmod(temp+1, 2.0) - 1) 
 
    for i in range(2, 16): 
        temp = ord(key[i]) + c1_value * y_array[i - 1] + c2_value * y_array[i - 2] 
        y_array.append(math.fmod(temp+1, 2.0) - 1) 
 
    for i in range(16): 
        if i == 14: 
            print("c1Prime: " + str(y_array[i])) 
        elif i == 15: 
            print("c2Prime: " + str(y_array[i])) 
        else: 
            print(str(y_array[i])) 
    c1Prime = y_array[14] 
    c2Prime = y_array[15] 
    return c1Prime, c2Prime


def f(x: float) -> float:
    return ((x + 1) % 2) - 1

def normalized(value): 
    return (value - 127.5) / 127.5

def denormalized(value):
    return round((value * 127.5) + 127.5)

def encrypt_value(value, y1, y2, c1Prime, c2Prime):
    return f(value + c1Prime * y1 + c2Prime * y2)

def decrypt_value(value, y1, y2, c1Prime, c2Prime):
    return f(value - c1Prime * y1 - c2Prime * y2)

def encrypt_func(key, original_values):
    normalized_original_values = []
    encrypted_values = []
    denormalized_encrypted_values = []
    c1Prime, c2Prime = key_func(key)
    #Convert Values [0,255] to Values [-1,1]
    for i in range(len(original_values)): 
        normalized_original_values.append(normalized(original_values[i])) 

    #First Index , using While True to organize variables
    while True:
        temp_encrypted_value = encrypt_value(normalized_original_values[0], y1_value, y2_value, c1Prime, c2Prime)
        temp_denormalized_encrypted_value = normalized(denormalized(temp_encrypted_value)) # NORMALIZED_CEPTION

        # print("Encrypted: " + str(temp_denormalized_encrypted_value))
        # print("Original: " + str(normalized_original_values[0])) 

        encrypted_values.append(temp_denormalized_encrypted_value)
        break

    #Second Index , using While True to organize variables
    while True:
        temp_encrypted_value = encrypt_value(normalized_original_values[1], encrypted_values[0], y1_value, c1Prime, c2Prime)
        temp_denormalized_encrypted_value = normalized(denormalized(temp_encrypted_value)) # NORMALIZED_CEPTION

        # print("Encrypted: " + str(temp_denormalized_encrypted_value)) 
        # print("Original: " + str(normalized_original_values[1])) 

        encrypted_values.append(temp_denormalized_encrypted_value) 
        break
    
    #The Rest of the Indexes
    for i in range(2, len(normalized_original_values)):
        while True:
            temp_encrypted_value = encrypt_value(normalized_original_values[i], encrypted_values[i - 1], encrypted_values[i - 2], c1Prime, c2Prime)
            temp_denormalized_encrypted_value = normalized(denormalized(temp_encrypted_value)) # NORMALIZED_CEPTION

            # print("Encrypted: " + str(temp_denormalized_encrypted_value)) 
            # print("Original: " + str(normalized_original_values[i])) 

            encrypted_values.append(temp_denormalized_encrypted_value)
            break
    
    # Denormalized to [0, 255]
    for i in range(len(encrypted_values)):
        denormalized_encrypted_values.append(denormalized(encrypted_values[i]))

    return denormalized_encrypted_values

def decrypt_func(key, encrypted_values):
    normalized_encrypted_values = []
    decrypted_values = []
    denormalized_decrypted_values = []
    c1Prime, c2Prime = key_func(key)
    #Convert Values [0,255] to Values [-1,1]
    for i in range(len(encrypted_values)): 
        normalized_encrypted_values.append(normalized(encrypted_values[i])) 

    #First Index
    decrypted_values.append(decrypt_value(normalized_encrypted_values[0], y1_value, y2_value, c1Prime, c2Prime))
    #Second Index
    decrypted_values.append(decrypt_value(normalized_encrypted_values[1], normalized_encrypted_values[0], y1_value, c1Prime, c2Prime))

    #The Rest of the Indexes
    for i in range(2, len(normalized_encrypted_values)): 
        decrypted_values.append(decrypt_value(normalized_encrypted_values[i], normalized_encrypted_values[i - 1], normalized_encrypted_values[i - 2], c1Prime, c2Prime))

    # Denormalized to [0, 255]
    for i in range(len(decrypted_values)):
        denormalized_decrypted_values.append(denormalized(decrypted_values[i]))
        
    return denormalized_decrypted_values

def encrypt_text(key, original_text):
    print("==== Start Text Encryption Process ====")
    print("\nOriginal Text: " + original_text)
    
    original_values = []
    denormalized_encrypted_values = []
    encrypted_text = ""
    
    #Convert ASCII Text to Values [0,255]
    for i in range(len(original_text)): 
        original_values.append(ord(original_text[i]))  

    denormalized_encrypted_values = encrypt_func(key, original_values) 

    for i in range(len(denormalized_encrypted_values)):
        encrypted_text += chr(denormalized_encrypted_values[i])
    print("\nEncrypted Text: " + encrypted_text)
    print("==== End Text Encryption Process ====")
    return encrypted_text

def decrypt_text(key, encrypted_text):
    print("==== Start Text Decryption Process ====")
    print("\nEncrypted Text: " + encrypted_text)

    encrypted_values = []
    denormalized_decrypted_values = []
    decrypted_text = ""
    
    #Convert ASCII Text to Values [0,255]
    for i in range(len(encrypted_text)): 
        encrypted_values.append(ord(encrypted_text[i]))  

    denormalized_decrypted_values = decrypt_func(key, encrypted_values) 

    for i in range(len(denormalized_decrypted_values)):
        decrypted_text += chr(denormalized_decrypted_values[i])

    print("\nDecrypted Text: " + decrypted_text)
    print("==== End Text Decryption Process ====")
    return decrypted_text  

import numpy as np
from PIL import Image

def encrypt_image(key, original_image):
    print("==== Start Image Encryption Process ====") 
    # Check if the image is loaded successfully
    if original_image is None:
        print("Error: Unable to load the image.")
        return None
    else:
        # Reshape the image array to a one-dimensional array
        flattened_image = original_image.ravel() # -1 means automatic calculation of the size

        # Print the flattened array of pixel values
        print("Flattened pixel values array:\n", flattened_image) 
        print("Original Length: " + str(len(flattened_image)))

        print("Encrypt: ")
        encrypted_image = encrypt_func(key, flattened_image)
        encrypted_image = np.reshape(encrypted_image, original_image.shape)
        # Print the flattened array of pixel values
        print("Encrypted pixel values array:\n", encrypted_image) 
        print("Encrypted Length: " + str(len(encrypted_image))) 
        return encrypted_image
 
def decrypt_image(key, encrypted_image):   
    print("==== Start Image Encryption Process ====") 
    # Check if the image is loaded successfully
    if encrypted_image is None:
        print("Error: Unable to load the image.")
        return None
    else:
        # Reshape the image array to a one-dimensional array
        flattened__encrypted_image = encrypted_image.ravel() # -1 means automatic calculation of the size 

        print("Decrypt: ") 
        
        decrypted_image = decrypt_func(key, flattened__encrypted_image)
        decrypted_image = np.reshape(decrypted_image, encrypted_image.shape)
        # Print the flattened array of pixel values
        print("Decrypted pixel values array:\n", decrypted_image) 
        print("Decrypted Length: " + str(len(decrypted_image))) 
        return decrypted_image

# Example Usage
key = "adabefgbfjklmnop"
original_image_path = "original_image.png"
encrypted_image_path = "encrypted_image.png"
decrypted_image_path = "decrypted_image.png"

# encrypt_image(key, cv2.imread(original_image_path))
# decrypt_image(key, cv2.imread(encrypted_image_path))