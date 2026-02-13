import numpy as np
from scipy.stats import poisson

def calc_probs(lambda_home, lambda_away, max_goals=6):
    ph = [poisson.pmf(i, lambda_home) for i in range(max_goals+1)]
    pa = [poisson.pmf(j, lambda_away) for j in range(max_goals+1)]
    matrix = np.outer(ph, pa)
    p_home = np.sum(np.tril(matrix, -1))
    p_draw = np.sum(np.diag(matrix))
    p_away = np.sum(np.triu(matrix, 1))
    return p_home, p_draw, p_away

def calc_ev(odds, prob):
    return round(odds * prob - 1, 3)

def ev_to_units(ev):
    if ev < 0.05: return 1
    elif ev < 0.10: return 2
    elif ev < 0.15: return 3
    elif ev < 0.20: return 4
    else: return 5
