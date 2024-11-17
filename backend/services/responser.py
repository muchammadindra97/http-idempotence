from flask import jsonify, Response


def validation_error(errors: dict[str, str]) -> tuple[Response, int]:
    return jsonify({
        'messages': 'Please check your input',
        'errors': errors
    }), 400


def basic(message: str, code=200) -> tuple[Response, int]:
    return jsonify({
        'messages': message
    }), code


def resources(data, message='Success to get data', code=200) -> tuple[Response, int]:
    return jsonify({
        'messages': message,
        'data': data
    }), code
