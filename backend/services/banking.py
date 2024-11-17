from flask import Blueprint, request
from backend.services.database import get_db
import backend.services.validator as validator
import backend.services.responser as responser

bp = Blueprint('banking', __name__)

@bp.post('/deposit')
def deposit():
    headers_validation = validator.validate({
        'Idempotency-Key': request.headers.get('Idempotency-Key', '')
    }, {
        'Idempotency-Key': ['required', 'idempotence']
    })

    if not headers_validation['is_valid']:
        return responser.validation_error(headers_validation['errors'], 'Please check your headers', 409)

    idempotency_key = headers_validation['validated']['Idempotency-Key']

    validation = validator.validate(request.json, {
        'amount': ['required', 'number', 'min:1']
    })

    if not validation['is_valid']:
        return responser.validation_error(validation['errors'])

    amount = validation['validated']['amount']

    db = get_db().cursor()
    db.execute(f"INSERT INTO account (amount, action, time) VALUES ({amount}, 'DEPOSIT', DATETIME())")
    db.execute(f"INSERT INTO idempotence_key (key, time) VALUES ('{idempotency_key}', DATETIME())")
    db.connection.commit()

    return responser.basic('Deposit success', 200)

@bp.post('/withdraw')
def withdraw():
    headers_validation = validator.validate({
        'Idempotency-Key': request.headers.get('Idempotency-Key', '')
    }, {
        'Idempotency-Key': ['required', 'idempotence']
    })

    if not headers_validation['is_valid']:
        return responser.validation_error(headers_validation['errors'], 'Please check your headers', 409)

    idempotency_key = headers_validation['validated']['Idempotency-Key']

    validation = validator.validate(request.json, {
        'amount': ['required', 'number', 'min:1']
    })

    if not validation['is_valid']:
        return responser.validation_error(validation['errors'])

    amount = validation['validated']['amount']
    balance = get_balance()

    if amount > balance:
        return responser.basic('Balance insufficient', 400)

    db = get_db().cursor()
    db.execute(f"INSERT INTO account (amount, action, time) VALUES (-{amount}, 'WITHDRAW', DATETIME())")
    db.execute(f"INSERT INTO idempotence_key (key, time) VALUES ('{idempotency_key}', DATETIME())")
    db.connection.commit()

    return responser.basic('Withdraw success', 200)

@bp.get('/history')
def history():
    db = get_db().cursor()
    result = []

    for raw_row in db.execute("SELECT id, amount, action, time FROM account ORDER BY time DESC").fetchall():
        row = {
            'id': raw_row[0],
            'amount': raw_row[1],
            'action': raw_row[2],
            'time': raw_row[3]
        }

        result.append(row)

    return responser.resources(result)

@bp.get('/balance')
def balance():
    balance = get_balance()

    return responser.resources({
        'balance': balance
    })

def get_balance():
    db = get_db().cursor()
    return db.execute("SELECT IFNULL(SUM(amount), 0) AS balance FROM account").fetchone()[0]