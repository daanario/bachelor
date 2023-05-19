
from numba import njit
from typing import List
import numpy as np
from itertools import combinations
from numba import njit
from typing import List

# Demand funktion for n-spillere. 
@njit
def demand(prices: List[float]) -> float:
    num_prices = len(prices)
    num_lower = 0
    num_equal = 0
    
    for price in prices[1:]:
        if prices[0] > price:
            num_lower += 1
        elif prices[0] == price:
            num_equal += 1
    if len(prices) == 1: 
        return 1.0 - prices[0]
    # Check om nogen priser er lavere end firma 0. 
    elif num_lower == num_prices - 1 and num_equal == 0:
        return 0.0
    # Hvis ikke, check hcor mange firmaer er lig firma 0.
    elif num_equal > 0:
        return 1.0 / (num_equal+1) * (1-prices[0])
    # Ellers for firma 0 hele markedet. 
    else:
        return 1.0 - prices[0]
    
    # Profit funktion for n-spillere. 
@njit
def profit(prices: List[float]) -> List[float]:
    return prices[0] * demand(prices)


# Find unikke kombinationer. 
def find_unique_combinations(lst, n):
    unique_combinations = set()
    for combination in combinations(lst, n):
        unique_combinations.add(tuple(sorted(combination)))
    return unique_combinations

# Setup prisgrids for n-spillere og k priser. 
two_player = np.linspace(0, 7/12, 8) #k = 48
three_player = np.linspace(0, 8/12, 9)#k = 48 
unique_representations_two = find_unique_combinations(two_player, 2)
unique_representations_three = find_unique_combinations(three_player, 3)

# Find unikke kombinationer. 

def find_unique_combinations(lst, n):
    unique_combinations = set()
    for combination in combinations(lst, n):
        unique_combinations.add(tuple(sorted(combination)))
    return unique_combinations


# Beregn profitter og gem i en liste.  
def benchmark_two_player(lst):
    unique = find_unique_combinations(lst, 2)
    unique_profits = set()
    for combination in unique:
        unique_profits.add(profit(combination))
    # Beregn totale profit
    total_profit = sum(unique_profits)
    # Regn gennemsnitlig pris pr. periode pr. firma
    avg_profit = total_profit/2/len(lst)
    return avg_profit

def benchmark_three_player(lst):
    # Beregn profitter og gem i en liste. 
    unique = find_unique_combinations(lst, 3)
    unique_profits = set()
    for combination in unique:
        unique_profits.add(profit(combination))
    # Beregn totale profit
    total_profit = sum(unique_profits)
    # Regn gennemsnitlig pris pr. periode pr. firma
    avg_profit = total_profit/3/len(lst)
    return avg_profit