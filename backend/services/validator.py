def run_rule(value: str, rule: str) -> bool:
    if rule == 'required':
        return rule != '' and rule is not None
    elif rule == 'number':
        return run_rule(value, 'required') and value.isdigit()
    elif 'min' in rule:
        number = int(rule.split(':')[1])
        return int(value) >= number
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
    else:
        return ''

def validate(data: dict, rules: dict[str, list[str]]) -> dict:
    result = {
        'is_valid': False,
        'validated': dict(),
        'errors': dict()
    }
    for key in rules.keys():
        value = data.get(key)
        for rule in rules.get(key):
            is_valid = run_rule(str(value), rule)
            if not is_valid:
                message = get_message(key, rule)
                result['errors'][key] = message
                continue
            result['validated'][key] = value

    result['is_valid'] = len(result['errors']) <= 0
    if result['is_valid']:
        result.pop('errors')
    else:
        result.pop('validated')

    return result
