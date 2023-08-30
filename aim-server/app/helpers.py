from flask import jsonify

def errorJson(errorMsg, code = 403):
    error_data = {"code": f"{code}", "message": errorMsg}
    return jsonify(error_data), code
