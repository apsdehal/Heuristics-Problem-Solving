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
