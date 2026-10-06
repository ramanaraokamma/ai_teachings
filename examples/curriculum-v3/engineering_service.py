"""Offline Grade 11 fixtures. No network, credentials or real side effects.

The role parameter simulates an already-authenticated server session; it is not
an authentication implementation and must not be populated from user JSON.
"""
from copy import deepcopy
import re


def nonnegative_integer(value):
    return type(value) is int and value >= 0


def validate_request(value):
    if type(value) is not dict or set(value) != {'room_id', 'requested_count'}:
        raise ValueError('request fields')
    if type(value['room_id']) is not str or not value['room_id']:
        raise ValueError('room ID')
    if not nonnegative_integer(value['requested_count']):
        raise ValueError('requested count')
    return dict(value)


def validate_identifier(value):
    # A separate, stricter Week 18 identifier exercise.
    return type(value) is str and re.fullmatch(r'[A-Z][0-9]', value) is not None


def may_read(role, resource_role):
    if role not in ('student', 'teacher') or resource_role not in ('student', 'teacher'):
        return False
    return role == 'teacher' or resource_role == 'student'


def remaining(capacity, used):
    if not nonnegative_integer(capacity) or not nonnegative_integer(used) or used > capacity:
        raise ValueError('capacity/used')
    return capacity - used


def report(request, role, records, trace):
    request = validate_request(request)
    if role not in ('student', 'teacher'):
        trace.append(('denied', 'session'))
        return {'status': 'denied'}
    room = request['room_id']
    # Filter before source contents enter lookup/output processing.
    eligible = [r for r in records if may_read(role, r['role']) and r['current']]
    trace.append(('lookup', room))
    approvals = [r for r in eligible if r['kind'] == 'approval' and r['room'] == room]
    registers = [r for r in eligible if r['kind'] == 'register' and r['room'] == room]
    if len(approvals) != 1 or len(registers) != 1:
        return {'status': 'needs_review', 'room': None, 'capacity': None, 'source_ids': []}
    capacity = registers[0]['capacity']
    if not nonnegative_integer(capacity):
        return {'status': 'needs_review', 'room': None, 'capacity': None, 'source_ids': []}
    return {'status': 'supported', 'room': room, 'capacity': capacity,
            'source_ids': [approvals[0]['id'], registers[0]['id']]}


def read_resource(role, resource, trace):
    if not may_read(role, resource['role']):
        trace.append(('denied', resource['id']))
        return None
    trace.append(('read', resource['id']))
    return resource['content']


def cache_key(query, role, corpus_version, procedure_version):
    return query, role, corpus_version, procedure_version


def cache_valid(age, ttl, saved_version, current_version):
    return 0 <= age < ttl and saved_version == current_version


def transition(state, target):
    allowed = {'ready': {'looking_up'}, 'looking_up': {'review', 'done'},
               'review': {'done'}, 'done': set()}
    if target not in allowed.get(state, set()):
        raise ValueError('invalid transition')
    return target


def waiting_bound(attempts, per_attempt, gaps):
    if type(attempts) is not int or attempts < 1 or len(gaps) != attempts - 1:
        raise ValueError('attempt budget')
    if per_attempt < 0 or any(g < 0 for g in gaps):
        raise ValueError('negative duration')
    return attempts * per_attempt + sum(gaps)


class MockLedger:
    """In-memory classroom deduplication, not durable exactly-once delivery."""
    def __init__(self):
        self.committed = {}
        self.effects = []

    def submit(self, key, payload, approval):
        if approval != payload:
            raise PermissionError('exact approval required')
        if key in self.committed:
            original, result = self.committed[key]
            if original != payload:
                raise ValueError('idempotency conflict')
            return deepcopy(result)
        result = {'operation_id': key, 'status': 'committed'}
        self.effects.append(deepcopy(payload))
        self.committed[key] = deepcopy(payload), deepcopy(result)
        return deepcopy(result)


if __name__ == '__main__':
    fixtures = [
        {'id': 'P', 'role': 'student', 'current': True, 'kind': 'approval', 'room': 'A'},
        {'id': 'R', 'role': 'student', 'current': True, 'kind': 'register', 'room': 'A', 'capacity': 12},
    ]
    trace = []
    print(report({'room_id': 'A', 'requested_count': 5}, 'student', fixtures, trace))
    print('Operation trace:', trace)
