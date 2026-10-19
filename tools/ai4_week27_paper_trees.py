def majority(rows):
    labels = [row[2] for row in rows]
    return 'blocked' if labels.count('blocked') > labels.count('clear') else 'clear'


def fit_node(rows, remaining_depth, feature=0):
    if not rows:
        raise ValueError('This fixture requires a nonempty node')
    fallback = majority(rows)
    if remaining_depth == 0 or len({row[2] for row in rows}) == 1:
        return {'label': fallback}
    children = {}
    for value in (0, 1):
        subset = [row for row in rows if row[feature] == value]
        children[value] = (fit_node(subset, remaining_depth - 1, feature + 1)
                           if subset else {'label': fallback})
    return {'feature': feature, 'children': children}


def predict(features, tree):
    if len(features) != 2 or any(type(x) is not int or x not in (0, 1) for x in features):
        raise ValueError('Need both binary flags in near/tall order')
    while 'label' not in tree:
        tree = tree['children'][features[tree['feature']]]
    return tree['label']


# Unique trip IDs are printed in the lesson table; tuples hold near,tall,reference.
training = [(0, 0, 'clear'), (0, 1, 'clear'),
            (1, 0, 'blocked'), (1, 1, 'clear')]
validation = [(0, 0, 'clear'), (0, 1, 'clear'),
              (1, 0, 'clear'), (1, 1, 'blocked')]
# Human-declared question order: near first, then tall; leaf ties choose clear.
for depth in [0, 1, 2]:
    tree = fit_node(training, depth)
    train_correct = sum(predict(row[:2], tree) == row[2] for row in training)
    valid_correct = sum(predict(row[:2], tree) == row[2] for row in validation)
    print(depth, train_correct, len(training), valid_correct, len(validation))
# Caller must supply complete binary training tuples/allowed labels and depth0..2.
# This is a constrained classroom fitter, not a general optimized tree algorithm.
