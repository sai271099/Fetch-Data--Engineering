import hashlib
import base64

def mask_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def base64_encode(string_parameter, action="encode"):
    """Function to encode or decode string using base64"""

    # Check if action is encoding or decoding
    if action == "encode":
        # Encode string to ASCII value
        ascii_string = string_parameter.encode('ascii')

        # Encode ASCII string to base64
        encoded_string = base64.b64encode(ascii_string).decode('utf-8')

        # Return the encoded string
        return encoded_string

    # Else decode the encrypted string
    elif action == "decode":
        # Decode base64 encrypted string
        decoded_string = base64.b64decode(string_parameter).decode('utf-8')

        # Return the decoded string
        return decoded_string
