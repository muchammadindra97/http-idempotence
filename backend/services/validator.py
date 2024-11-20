from backend.services.database import get_db

def run_rule(value: str, rule: str) -> bool:
    if rule == 'required':
        return value != '' and value is not None
    elif rule == 'number':
        return run_rule(value, 'required') and value.isdigit()
    elif 'min' in rule:
        number = int(rule.split(':')[1])
        return int(value) >= number
    elif rule == 'idempotence':
        return not is_idempotence_key_used(value)
    else:
        return True

def get_message(key: str, rule: str) -> str:
    if rule == 'required':
        return f'field {key} is required'
    elif rule == 'number':
        return f'field {key} must be number'
    elif 'min' in rule:
        number = int(rule.split(':')[1])
        return f'field {key} must be greater than {number}'
    elif rule == 'idempotence':
        return f'field {key} is already processed'
    else:
        return ''

def validate(data: dict, rules: dict[str, list[str]]) -> dict:
    result = {
        'is_valid': False,
        'validated': dict(),
        'errors': dict(),
        'violated_rule': dict()
    }
    for key in rules.keys():
        value = data.get(key)
        for rule in rules.get(key):
            is_valid = run_rule(str(value), rule)
            if not is_valid:
                message = get_message(key, rule)
                result['errors'][key] = message
                result['violated_rule'][key] = rule
                break
            result['validated'][key] = value

    result['is_valid'] = len(result['errors']) <= 0
    if result['is_valid']:
        result.pop('errors')
        result.pop('violated_rule')
    else:
        result.pop('validated')

    return result

def is_idempotence_key_used(key: str) -> bool:
    expiry = '1 minutes'
    db = get_db().cursor()
    return db.execute(f"SELECT key FROM idempotence_key WHERE key = '{key}' AND time >= DATETIME('now', '-{expiry}')").fetchone() is not None