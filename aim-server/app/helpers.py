def errorJson(dataType, code = 403):
    error_data = {"code": f"{code}", "message": f"Must provide {dataType}"}
    return jsonify(error_data), {code}
