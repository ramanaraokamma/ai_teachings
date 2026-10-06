"""Check the constructed Grade 9 capstone examples independently of answer text."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def mse(weight, rows):
    return sum((max(0, weight * x) - y) ** 2 for x, y in rows) / len(rows)


def fit(target_scale, rate):
    # Compute gradients from the two individual training rows.
    weight = 1.0
    checkpoints = []
    for _ in range(2):
        gradient = sum(2 * (weight * x - target_scale * x) * x for x in (1, 2)) / 2
        weight -= rate * gradient
        checkpoints.append(weight)
    return checkpoints


def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), (actual, expected)


roadmap = json.loads((ROOT / 'curriculum-v3/progression.json').read_text())
for week in range(33, 37):
    chapter = json.loads((ROOT / f'curriculum-v3/ai-4-week-{week:02}.json').read_text())
    assert chapter['title'] == roadmap['levels'][3]['weeks'][week - 1]
    assert chapter['level'] == 'ai-4' and chapter['week'] == week
    assert chapter['minutes'] == 90 and len(chapter['goals']) == 3
    assert len(chapter['lesson']) == len(chapter['workbook']) == 5
    assert len(chapter['teacher']['sessions']) == 8
    assert [t['id'] for t in chapter['workbook']] == ['W1', 'W2', 'W3', 'W4', 'W5']
    blocks = [b for section in chapter['lesson'] for b in section['blocks']]
    assert sum(b['type'] == 'diagram' for b in blocks) == 1
    student_text = json.dumps(chapter['lesson'])
    for task in chapter['workbook']:
        assert task['prompt'] and task['answer'] and task['lines'] >= 4
        assert task['answer'] not in student_text

# Main, independent and fresh-retry validation cases.
for scale, expected_baseline, expected_slow in [(2, 12.5, .78125), (3, 50, 3.125), (4, 112.5, 7.03125)]:
    rows = [(3, scale * 3), (4, scale * 4)]
    slow, fast = fit(scale, .1), fit(scale, .2)
    close(mse(1, rows), expected_baseline)
    close(mse(slow[-1], rows), expected_slow)
    close(mse(fast[-1], rows), 0)
    close(fast[-1], scale)
close(fit(2, .3)[-1], 1.75)

# Main, independent and retry frozen final tests.
for scale, baseline, candidate, negative in [(2, 20.25, 5, 10), (3, 31.25, 11.25, 22.5), (4, 65, 20, 40)]:
    positive_inputs = (5, 6) if scale == 2 else (2, 4)
    rows = [(x, scale * x) for x in (*positive_inputs, -1, -2)]
    close(mse(1, rows), baseline)
    close(mse(scale, rows), candidate)
    close(mse(scale, rows[-2:]), negative)
    assert all(max(0, scale * x) == 0 for x in (-1, -2))

for before, after, relative in [([4, 9, 1, 2], [1, 1, 2, 0], .75), ([9, 9, 1, 1], [1, 1, 0, 2], .8)]:
    close((sum(before) - sum(after)) / sum(before), relative)
    assert len(before) == len(after) == 4

print('Grade 9 capstone: schema, arithmetic, independent cases and fresh retries passed.')
