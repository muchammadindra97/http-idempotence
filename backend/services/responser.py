from flask import jsonify, Response


def validation_error(errors: dict[str, str], message: str = 'Please check your input', code=400) -> tuple[Response, int]:
    return jsonify({
        'message': message,
        'errors': errors
    }), code


def basic(message: str, code=200) -> tuple[Response, int]:
    return jsonify({
        'message': message
    }), code


def resources(data, message='Success to get data', code=200) -> tuple[Response, int]:
    return jsonify({
        'message': message,
        'data': data
    }), code
