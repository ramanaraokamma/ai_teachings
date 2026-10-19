import json

class DuplicateField(ValueError):
    pass

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateField('duplicate field')
        result[key] = value
    return result

def reject_constant(token):
    raise ValueError('non-JSON numeric constant')

def validate_activity(text):
    # This lesson supplies short text cards, not unbounded network input.
    rejected = {'accepted': False, 'minutes': None}
    try:
        record = json.loads(text, object_pairs_hook=unique_object,
                            parse_constant=reject_constant)
    except DuplicateField:
        return 'duplicate-field policy', rejected
    except (json.JSONDecodeError, ValueError):
        return 'syntax', rejected
    if type(record) is not dict:
        return 'schema: top-level object', rejected
    if set(record) != {'name', 'minutes'}:
        return 'schema: exact fields', rejected
    if type(record['name']) is not str or len(record['name']) == 0:
        return 'schema: name', rejected
    if type(record['minutes']) is not int:
        return 'schema: integer minutes', rejected
    if not 0 <= record['minutes'] <= 60:
        return 'schema: minutes range', rejected
    return 'accepted', {'accepted': True, 'minutes': record['minutes']}

cards = [
    '{"name":"Sketch","minutes":12}',
    '{name:"Sketch","minutes":12}',
    '[]',
    '{"name":"Sketch"}',
    '{"name":"Sketch","minutes":"12"}',
    '{"name":"Sketch","minutes":true}',
    '{"name":"Sketch","minutes":61}',
    '{"name":"Sketch","minutes":0}',
]
for number, text in enumerate(cards, 1):
    status, result = validate_activity(text)
    print(number, status, json.dumps(result, allow_nan=False))
