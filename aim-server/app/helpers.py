from flask import jsonify

def errorJson(errorMsg, code = 403):
    error_data = {"code": f"{code}", "message": errorMsg}
    return jsonify(error_data), code

def has_required_chars(password):
    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if the password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check if the password contains at least one special symbol
    special_symbols = "!@#$%^&*()_-+=<>?/[]{}"
    if not any(char in special_symbols for char in password):
        return False

    return True