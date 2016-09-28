# Fixed options
_algorithms = ('Adaptive', 'Non-adaptive')
_weighFuncs = ('Gaussian', 'Linear', 'JSD')
_directions = ('Forward', 'Backward')
_boostMethods = ('Sum similarity', 'Counts')
_yesNo = ('Yes', 'No')


def validatestr(value):
    '''Validate that given value is a non-empty string. Used to validate
    tracker parameters.'''
    try:
        s = str(value)
        return None if (len(s) == 0) else s
    except:
        raise ValueError


def _isValidOption(value, options):
    '''Validate that given value is a string from a predetermined set.
    Used to validate tracker parameters.'''
    if value in options:
        return value
    else:
        raise ValueError


def validAlgorithm(value):
    '''Validate algorithm -- in lower case'''
    return _isValidOption(value, _algorithms).lower()


def validWeighting(value):
    '''Validate weighting function'''
    return _isValidOption(value, _weighFuncs)


def validDirection(value):
    '''Validate direction is Forward (false means backward)'''
    return _isValidOption(value, _directions) == 'Forward'


def sumSimilarity(value):
    '''Validate boost methods is Sum distances (false means Counts)'''
    return _isValidOption(value, _boostMethods) == 'Sum similarity'


def validCleaning(value):
    return _isValidOption(value, _yesNo) == 'Yes'
