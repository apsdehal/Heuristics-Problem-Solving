import numpy as np

def binary_candidate_score_to_msg(score, candidate):
    msg = '%+1.4f:' % score

    strings = []
    for attr in candidate:
        strings += '%1d' % attr

    msg += ','.join(strings) + '\n'
    return msg

def parseCandidateData(data):
    score = float(data[:7])
    candidate = [float (x) for x in data[8:][:-1].split(',')]
    return (candidate, score)

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
    total_nums = n
    pos_nums = 38*total_nums/100
    neg_nums = total_nums - pos_nums
    mlist_pos = np.random.random(pos_nums)
    sum =0
    for i in mlist_pos:
        sum += i
    newSum = 0
    maxVal = 0
    minVal = 1
    maxValIndex = 0
    minValIndex = 0
    for index, item in enumerate(mlist_pos):
        mlist_pos[index]=round(item/sum,2)
        newSum += mlist_pos[index]
        if(mlist_pos[index]>maxVal):
            maxVal = mlist_pos[index]
            maxValIndex = index
        if(mlist_pos[index]<minVal):
            minVal = mlist_pos[index]
            minValIndex = index
    diff = 1 - newSum
    if(diff>0):
        mlist_pos[minValIndex] = mlist_pos[minValIndex] + diff
    if(diff<0):
        mlist_pos[maxValIndex] = mlist_pos[maxValIndex] + diff

    #for negetive numbers
    mlist_neg = np.random.random(neg_nums)
    sum =0
    for i in mlist_neg:
        sum += i
    newSum = 0
    maxVal = 0
    minVal = 1
    maxValIndex = 0
    minValIndex = 0
    for index, item in enumerate(mlist_neg):
        temp=round(item/sum,2)
        mlist_neg[index]=-temp
        newSum += temp
        if(temp>maxVal):
            maxVal = temp
            maxValIndex = index
        if(temp<minVal):
            minVal = temp
            minValIndex = index
    diff = 1 - newSum
    if(diff>0):
        mlist_neg[minValIndex] = mlist_neg[minValIndex] - diff
    if(diff<0):
        mlist_neg[maxValIndex] = mlist_neg[maxValIndex] - diff

    mWeights = np.concatenate((mlist_pos, mlist_neg))
    np.random.shuffle(mWeights)
    return mWeights

def checkSum(weights):
    sum_pos = np.sum(np.array([w for w in weights if w>=0]))
    sum_neg = np.sum(np.array([w for w in weights if w < 0]))
    if not np.isclose(sum_pos, 1):
        return False
    if not np.isclose(sum_neg, -1):
        return False
    return True 