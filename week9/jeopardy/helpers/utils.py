import numpy as np

def binary_candidate_score_to_msg(score, candidate):
    msg = '%+1.4f:' % score

    strings = []
    for attr in candidate:
        strings += '%1d' % attr

    msg += ','.join(strings) + '\n'
    return msg


def floats_to_msg4(arr):
    'Convert float array to proper msg format with 4 decimals'

    strings = []
    for a in arr:
        strings.append('%+01.4f' % a)
    msg = ','.join(strings) + '\n'
    return msg


def floats_to_msg2(arr):
    'Convert float array to proper msg format with 2 decimals'

    strings = []
    for a in arr:
        strings.append('%+01.2f' % a)
    msg = ','.join(strings) + '\n'
    return msg


def candidate_to_msg(arr):
    'Convert a candidate to proper msg format'

    strings = []
    for a in arr:
        strings.append('%d' % a)
    msg = ','.join(strings) + '\n'
    return msg


def get_valid_prob(n):
    alpha = np.random.random(n)
    p = np.random.dirichlet(alpha)
    p = np.trunc(p*100)/100.0

    # ensure p sums to 1 after rounding
    p[-1] = 1 - np.sum(p[:-1])
    return p


def get_valid_weights(n):
    half = n/2

    a = np.zeros(n)
    a[:half] = get_valid_prob(half)
    a[half:] = -get_valid_prob(n - half)
    return np.around(a, 2)
