"""Offline constructed Grade 12 arithmetic with explicit model assumptions."""
from itertools import combinations, product
from math import sqrt


def sample_means(population, size):
    if type(size) is not int or not 1 <= size <= len(population):
        raise ValueError('sample size')
    # Index units separately even where values are identical.
    return [sum(population[i] for i in indices) / size
            for indices in combinations(range(len(population)), size)]


def known_sigma_interval(mean, sigma, n, critical=1.96):
    """Assume independent normal sampling and a known population sigma."""
    if type(n) is not int or n < 1 or sigma < 0 or critical <= 0:
        raise ValueError('interval settings')
    se = sigma / sqrt(n)
    margin = critical * se
    return se, mean - margin, mean + margin


def sign_flip_p(differences):
    """Two-sided exact test under independent symmetric sign exchangeability.

    Tiny n only; hold absolute magnitudes fixed and include equal extremes.
    A p-value is not a posterior probability that the null is true.
    """
    if not differences or len(differences) > 16:
        raise ValueError('require 1–16 paired units')
    threshold = abs(sum(differences))
    count = 0
    for signs in product((-1, 1), repeat=len(differences)):
        simulated = abs(sum(s * abs(d) for s, d in zip(signs, differences)))
        if simulated >= threshold - 1e-12:
            count += 1
    return count / (2 ** len(differences))


def bonferroni(p_values, alpha=.05):
    if not p_values or not 0 < alpha < 1 or any(not 0 <= p <= 1 for p in p_values):
        raise ValueError('test settings')
    threshold = alpha / len(p_values)
    return threshold, [p <= threshold for p in p_values]


def paired_gain(baseline, candidate):
    if not baseline or len(baseline) != len(candidate):
        raise ValueError('paired lengths')
    differences = [a - b for a, b in zip(baseline, candidate)]
    return differences, sum(differences) / len(differences)


if __name__ == '__main__':
    print('Six sample means:', sample_means([1, 1, 3, 3], 2))
    print('Known-sigma interval:', known_sigma_interval(10, 2, 16))
    print('Exact sign-flip p:', sign_flip_p([1, 1, 1]))
    print('Family decisions:', bonferroni([.009, .012, .3, .4, .8]))
