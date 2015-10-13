import numpy as np
from sklearn.metrics import make_scorer
from scipy.stats import sem

def ae(actual, predicted):
    """
    Computes the absolute error.

    This function computes the absolute error between two numbers,
    or for element between a pair of lists or numpy arrays.

    Parameters
    ----------
    actual : int, float, list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double or list of doubles
            The absolute error between actual and predicted

    """
    return np.abs(np.array(actual)-np.array(predicted))

def ce(actual, predicted):
    """
    Computes the classification error.

    This function computes the classification error between two lists

    Parameters
    ----------
    actual : list
             A list of the true classes
    predicted : list
                A list of the predicted classes

    Returns
    -------
    score : double
            The classification error between actual and predicted

    """
    return (sum([1.0 for x,y in zip(actual,predicted) if x != y]) /
            len(actual))

def mae(actual, predicted):
    """
    Computes the mean absolute error.

    This function computes the mean absolute error between two lists
    of numbers.

    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The mean absolute error between actual and predicted

    """
    return np.mean(ae(actual, predicted))

def mse(actual, predicted):
    """
    Computes the mean squared error.

    This function computes the mean squared error between two lists
    of numbers.

    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The mean squared error between actual and predicted

    """
    return np.mean(se(actual, predicted))

def msle(actual, predicted):
    """
    Computes the mean squared log error.

    This function computes the mean squared log error between two lists
    of numbers.

    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The mean squared log error between actual and predicted

    """
    return np.mean(sle(actual, predicted))

def rmse(actual, predicted):
    """
    Computes the root mean squared error.

    This function computes the root mean squared error between two lists
    of numbers.

    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The root mean squared error between actual and predicted

    """
    return np.sqrt(mse(actual, predicted))

def rmsle(actual, predicted):
    """
    Computes the root mean squared log error.

    This function computes the root mean squared log error between two lists
    of numbers.

    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The root mean squared log error between actual and predicted

    """
    return np.sqrt(msle(actual, predicted))

def se(actual, predicted):
    """
    Computes the squared error.

    This function computes the squared error between two numbers,
    or for element between a pair of lists or numpy arrays.

    Parameters
    ----------
    actual : int, float, list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double or list of doubles
            The squared error between actual and predicted

    """
    return np.power(np.array(actual)-np.array(predicted), 2)

def sle(actual, predicted):
    """
    Computes the squared log error.

    This function computes the squared log error between two numbers,
    or for element between a pair of lists or numpy arrays.

    Parameters
    ----------
    actual : int, float, list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double or list of doubles
            The squared log error between actual and predicted

    """
    return (np.power(np.log(np.array(actual)+1) - 
            np.log(np.array(predicted)+1), 2))

def ll(actual, predicted):
    """
    Computes the log likelihood.

    This function computes the log likelihood between two numbers,
    or for element between a pair of lists or numpy arrays.

    Parameters
    ----------
    actual : int, float, list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double or list of doubles
            The log likelihood error between actual and predicted

    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    err = np.seterr(all='ignore')
    score = -(actual*np.log(predicted)+(1-actual)*np.log(1-predicted))
    np.seterr(divide=err['divide'], over=err['over'],
              under=err['under'], invalid=err['invalid'])
    if type(score)==np.ndarray:
        score[np.isnan(score)] = 0
    else:
        if np.isnan(score):
            score = 0
    return score

def log_loss(actual, predicted):
    """
    Computes the log loss.

    This function computes the log loss between two lists
    of numbers.

    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The log loss between actual and predicted

    """
    return np.mean(ll(actual, predicted))

def rmspe(actual, predicted):
    """
    Computes the root mean square percentage error between two lists
    of numbers. Ignores elements where actual[n] == 0.
    
    Parameters
    ----------
    actual : list of numbers, numpy array
             The ground truth value
    predicted : same type as actual
                The predicted value

    Returns
    -------
    score : double
            The root mean squared percentage error between actual and predicted

    """
    
    actual = np.array(actual)
    predicted = np.array(predicted)
    zeros = actual == 0
    actual = actual[~zeros]
    predicted = predicted[~zeros]
    return np.sqrt(np.sum(np.power((actual - predicted) / actual, 2)) / len(actual))
    
def scorer(func, greater_is_better=True):
    return make_scorer(eval(func), greater_is_better=greater_is_better)

def display_scores(params, scores, append_star=False):
    """Format the mean score +/- std error for params"""
    params = ", ".join("{0}={1}".format(k, v)
                      for k, v in params.items())
    line = "{0}:\t\t{1:.3f} (+/-{2:.3f})".format(
        params, np.mean(scores), sem(scores))
    if append_star:
        line += " *"
    return line

def display_grid_scores(grid_scores, top=None):
    """Helper function to format a report on a grid of scores"""
    grid_scores = sorted(grid_scores, key=lambda x: x[1], reverse=True)
    if top is not None:
        grid_scores = grid_scores[:top]
        
    # Compute a threshold for staring models with overlapping stderr:
    _, best_mean, best_scores = grid_scores[0]
    threshold = best_mean - 2 * sem(best_scores)
    
    for params, mean_score, scores in grid_scores:
        append_star = mean_score + 2 * sem(scores) > threshold
        print(display_scores(params, scores, append_star=append_star))
