import numpy as np
import scipy.stats as ss


def weightJSD(Y1, Y2, offsetY=10):
    '''Jensen-Shannon divergense weighting. This estimates the JSD between two
    normal distributions with sigma=1, an mean located at Y1 and Y2
    respectively.

    Arguments:
    Y1,Y2        Years whose similarity we want to calculate.
    offsetY      Width of margin on time window.
    '''
    # Time window covers both target years, plus some margin
    minY = min(Y1, Y2) - offsetY
    maxY = max(Y1, Y2) + offsetY
    # Estimate JSD over range t
    t = np.linspace(minY, maxY)
    p = ss.norm.pdf(t, loc=Y1, scale=1)
    q = ss.norm.pdf(t, loc=Y2, scale=1)
    # Joint distribution
    m = 0.5 * (p + q)
    return 1 - max(0.5 * (ss.entropy(p, m) + ss.entropy(q, m)), 0)


def weightGauss(Y1, Y2, c=10):
    '''Gaussian function weighting. This calculates the similarity between Y1
    and Y2 as a Gaussian function of the difference between the years. The
    function peaks when Y1 == Y2 and tends to 0 as the difference increases.

    Arguments:
    Y1,Y2        Years whose similarity we want to calculate.
    c            This parameter controls the shape of the gaussian. Higher
                 values cause slower decay.
    '''
    x = Y1 - Y2
    return (np.exp(-(x ** 2) / c))


def weightLinear(Y1, Y2, a=10):
    '''Linear weighting. This calculates the similarity as a linear function of
    the difference between Y1 and Y2. The function peaks when Y1 == Y2 and
    linearly decays to 0 as the difference increases.

    Arguments:
    Y1,Y2        Years whose similarity we want to calculate.
    a            This parameter controls the speed of decay. Higher values
                 cause slower decay.
    '''
    return max(1 - abs(Y2 - Y1) / a, 0)
