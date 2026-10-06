"""Independent arithmetic and contract checks for AI 5 Weeks 1–12."""
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), (actual, expected)


def tokenise(text):
    vocabulary = {'cat': 1, 'c': 2, 'a': 3, 't': 4, 's': 5, ' ': 6, 'sat': 7}
    result, position = [], 0
    while position < len(text):
        matches = [token for token in vocabulary if text.startswith(token, position)]
        if not matches:
            return result, position
        token = max(matches, key=len)
        result.append(vocabulary[token])
        position += len(token)
    return result, None


def sample(probabilities, draw):
    assert F(0) <= draw < F(1)
    assert sum(probabilities) == 1 and all(p >= 0 for p in probabilities)
    total = F(0)
    for index, p in enumerate(probabilities):
        total += p
        if draw < total:
            return index
    raise AssertionError('Unassigned valid draw')


def sharpen(probabilities):
    squared = [p * p for p in probabilities]
    return [p / sum(squared) for p in squared]


def mix(values, weights):
    assert len(values) == len(weights) and sum(weights) == 1
    assert len({len(value) for value in values}) == 1
    return [sum(w * v[j] for v, w in zip(values, weights)) for j in range(len(values[0]))]


def softmax(scores):
    largest = max(scores)
    weights = [math.exp(s - largest) for s in scores]
    return [w / sum(weights) for w in weights]


def block(h, attention):
    z = [a + b for a, b in zip(h, attention)]
    branch = [max(0, value) for value in z]
    residual = [a + b for a, b in zip(z, branch)]
    return z, branch, residual


roadmap = json.loads((ROOT / 'curriculum-v3/progression.json').read_text())
for week in range(1, 13):
    w = json.loads((ROOT / f'curriculum-v3/ai-5-week-{week:02}.json').read_text())
    assert w['level'] == 'ai-5' and w['week'] == week and w['minutes'] == 90
    assert w['title'] == roadmap['levels'][4]['weeks'][week - 1]
    assert len(w['goals']) == 3 and len(w['lesson']) == len(w['workbook']) == 5
    assert len(w['teacher']['sessions']) == 8
    assert [t['id'] for t in w['workbook']] == ['W1', 'W2', 'W3', 'W4', 'W5']
    assert sum(b['type'] == 'diagram' for s in w['lesson'] for b in s['blocks']) == 1
    for t in w['workbook']:
        assert t['lines'] >= 4 and t['prompt'] and t['answer']

assert [F(n, 10) for n in (6, 3, 1)] == [F(3, 5), F(3, 10), F(1, 10)]
for text, result, failure in [('cats sat', [1, 5, 6, 7], None), ('sat cats', [7, 6, 1, 5], None), ('sat cat!', [7, 6, 1], 7), ('cats Cat', [1, 5, 6], 5), ('c at', [2, 6, 3, 4], None)]:
    assert tokenise(text) == (result, failure)

close(.5 * .8 + .3 * .5 + .2, .75)
close(.4 * .5 + .35 * .8 + .25, .73)
assert .6 * .51 < .4 * 1

base = [F(6, 10), F(3, 10), F(1, 10)]
sharp = sharpen(base)
assert sharp == [F(18, 23), F(9, 46), F(1, 46)]
assert [sample(base, F(n, 10)) for n in (2, 6, 9)] == [0, 1, 2]
assert [sample(sharp, F(n, 10)) for n in (2, 6, 9)] == [0, 0, 1]
assert sample(base, F(7, 10)) == 1 and sample(sharp, F(7, 10)) == 0
new = [F(5, 10), F(3, 10), F(2, 10)]
assert sharpen(new) == [F(25, 38), F(9, 38), F(4, 38)]
assert [sample(new, F(n, 10)) for n in (5, 9)] == [1, 2]
assert [sample(sharpen(new), F(n, 10)) for n in (5, 9)] == [0, 2]
retry = [F(4, 10), F(4, 10), F(2, 10)]
assert sharpen(retry) == [F(4, 9), F(4, 9), F(1, 9)]
assert [sample(sharpen(retry), F(n, 100)) for n in (40, 85)] == [0, 1]

for embeddings, positions, expected in [([[1, 2], [3, 0]], [[0, 1], [1, 0]], [5, 3]), ([[2, 0], [0, 4]], [[1, 0], [0, 2]], [3, 6])]:
    totals = []
    for ordered in [embeddings, embeddings[::-1]]:
        represented = [[a + b for a, b in zip(v, p)] for v, p in zip(ordered, positions)]
        totals.append([sum(v[j] for v in represented) for j in range(2)])
    assert totals == [expected, expected]

assert mix([[2, 0], [0, 4], [4, 2]], [F(1, 2), F(1, 4), F(1, 4)]) == [2, F(3, 2)]
assert mix([[2, 0], [0, 4]], [F(2, 3), F(1, 3)]) == [F(4, 3), F(4, 3)]
assert mix([[4, 1], [0, 5], [2, 3]], [F(1, 4), F(1, 2), F(1, 4)]) == [F(3, 2), F(7, 2)]
assert mix([[4, 1], [2, 3]], [F(1, 2), F(1, 2)]) == [3, 2]

for scores, expected in [([0, math.log(3)], [.25, .75]), ([0, math.log(2), math.log(3)], [1/6, 1/3, .5]), ([0, math.log(3), math.log(4)], [1/8, 3/8, .5])]:
    weights = softmax(scores)
    for actual, wanted in zip(weights, expected): close(actual, wanted)
    for original, shifted in zip(weights, softmax([s + 1000 for s in scores])): close(original, shifted)
close(sum(w * v for w, v in zip(softmax([0, math.log(2), math.log(3)]), [0, 3, 8])), 5)
close(sum(w * v for w, v in zip(softmax([0, math.log(3), math.log(4)]), [2, 6, 0])), 2.5)

assert block([1, 2], [3, -1]) == ([4, 1], [4, 1], [8, 2])
assert block([-2, 1], [1, -3]) == ([-1, -2], [0, 0], [-1, -2])
assert block([3, -2], [-5, 5]) == ([-2, 3], [0, 3], [-2, 6])
assert block([1, -3], [-4, 5]) == ([-3, 2], [0, 2], [-3, 4])
close(softmax([-8, 0])[0], .0003353501304664781)
close(softmax([-7, 0])[0], .0009110511944006454)

# Token-loss main, independent and fresh-retry cases.
for probabilities, expected in [([.8, .5], .4581453659370775), ([.6, .6], .5108256237659907), ([.5, .25], 1.0397207708399179), ([.25, .8], .8047189562170501), ([.4, .4], .916290731874155)]:
    close(-sum(math.log(p) for p in probabilities) / len(probabilities), expected)
assert 100 - 20 - 10 - 20 == 30 + 20 == 50
assert 120 - 25 - 15 - 30 == 28 + 22 == 50
assert 90 - 20 - 10 - 20 == 24 + 16 == 40


def check_schema(value, known_ids):
    if not isinstance(value, dict) or set(value) != {'status', 'room', 'capacity', 'source_ids'}:
        return False
    ids = value['source_ids']
    if not isinstance(ids, list) or any(type(i) is not str for i in ids):
        return False
    if len(set(ids)) != len(ids) or not set(ids) <= known_ids:
        return False
    if value['status'] == 'needs_review':
        return value['room'] is None and value['capacity'] is None
    if value['status'] != 'supported':
        return False
    return type(value['room']) is str and bool(value['room']) and type(value['capacity']) is int and value['capacity'] >= 0


def check_support(value, approval, register):
    return (value['room'] == approval['room'] == register['room']
            and value['capacity'] == register['capacity']
            and {approval['id'], register['id']} <= set(value['source_ids']))


valid = {'status': 'supported', 'room': 'F', 'capacity': 9, 'source_ids': ['A', 'B']}
approval = {'id': 'A', 'room': 'F'}
register = {'id': 'B', 'room': 'F', 'capacity': 9}
assert check_schema(valid, {'A', 'B'}) and check_support(valid, approval, register)
for bad_capacity in ('9', True, None, -1, 9.5):
    assert not check_schema({**valid, 'capacity': bad_capacity}, {'A', 'B'})
assert not check_schema({**valid, 'book_now': True}, {'A', 'B'})
assert not check_schema({k: v for k, v in valid.items() if k != 'capacity'}, {'A', 'B'})
assert not check_schema({**valid, 'source_ids': ['A', 'A']}, {'A', 'B'})
assert not check_schema({**valid, 'source_ids': ['A', 'Z']}, {'A', 'B'})
wrong_room = {**valid, 'room': 'G'}
assert check_schema(wrong_room, {'A', 'B'}) and not check_support(wrong_room, approval, register)
zero = {**valid, 'capacity': 0}
assert check_schema(zero, {'A', 'B'})
assert check_support(zero, approval, {**register, 'capacity': 0})
assert not check_support(zero, approval, register)
review = {**valid, 'status': 'needs_review', 'room': None, 'capacity': None}
assert check_schema(review, {'A', 'B'})
assert not check_schema({**review, 'room': 'F'}, {'A', 'B'})

print('AI 5 Weeks 1–12: structure, arithmetic, tokenisation, sampling, attention and response contracts passed.')
