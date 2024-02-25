# probability_calculator.py
import numpy as np
from decimal import Decimal, getcontext

global_precision = 100

def calculate_individual_probability(x_expr, N_expr, variables={}):
    global global_precision
    getcontext().prec = global_precision
    # Evaluate expressions for x and N using the provided variable values
    try:
        x_value = Decimal(eval(x_expr, {}, variables))
        N_value = Decimal(eval(N_expr, {}, variables))
    except NameError as e:
        raise ValueError(f"Undefined variable in expression: {e}")
    
    return Decimal(1) / (x_value ** N_value)

def calculate_total_probability(probability_factors, variables={}):
    global global_precision
    getcontext().prec = global_precision
    P_t = Decimal(1)
    for x_expr, N_expr in probability_factors:
        P_t *= calculate_individual_probability(x_expr, N_expr, variables)
    return P_t
