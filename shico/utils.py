import numpy as np


def weightJSD(Y1, Y2, offsetY=10):
    '''TODO: document!
    '''
    minY = min(Y1, Y2) - offsetY
    maxY = max(Y1, Y2) + offsetY
    t = np.linspace(minY, maxY)
    p = ss.norm.pdf(t, loc=Y1, scale=1)
    q = ss.norm.pdf(t, loc=Y2, scale=1)
    m = 0.5 * (p + q)
    return 1 - max(0.5 * (ss.entropy(p, m) + ss.entropy(q, m)), 0)


def weightGauss(Y1, Y2, c=10):
    '''TODO: document!
    '''
    x = Y1 - Y2
    return (np.exp(-(x ** 2) / c))


def weightLinear(Y1, Y2, a=10):
    '''TODO: document!
    '''
    return max(1 - abs(Y2 - Y1) / a, 0)
