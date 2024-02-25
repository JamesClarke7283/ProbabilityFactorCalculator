# probability_calculator.py
import numpy as np

def calculate_individual_probability(x_expr, N_expr, variables={}):
    # Evaluate expressions for x and N using the provided variable values
    try:
        x_value = eval(x_expr, {}, variables)
        N_value = eval(N_expr, {}, variables)
    except NameError as e:
        raise ValueError(f"Undefined variable in expression: {e}")
    
    return 1 / np.power(x_value, N_value)

def calculate_total_probability(probability_factors, variables={}):
    P_t = 1
    for x_expr, N_expr in probability_factors:
        P_t *= calculate_individual_probability(x_expr, N_expr, variables)
    
    if P_t == 0:
        return np.finfo(float).tiny
    return P_t
