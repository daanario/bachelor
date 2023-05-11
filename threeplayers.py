import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from numba import njit
from numba import jit
import numba as nb
from IPython.display import clear_output
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter

@njit
def demand(p1t, p2t, p3t):
    if (p1t < p2t) and (p1t<p3t):
        return 1 - p1t
    elif (p1t == p2t == p3t):
        return 1/3 * (1 - p1t)
    elif (p1t > p2t) or (p1t > p3t):
        return 0
    elif ((p1t < p2t) and (p1t == p3t)) or ((p1t == p2t) and (p1t < p3t)):
        return 1/2 * (1 - p1t)
    
@njit
def profit(p1t, p2t, p3t):
    return p1t * demand(p1t, p2t, p3t)
    
@njit
def set_price(i, t, p_table, Q_table, prices, epsilon):
    
    if epsilon >= np.random.uniform(0,1):
        
        return np.random.choice(prices)
    else:
        if i == 0:
            j = 1
            k = 2
        if i == 1:
            j = 2
            k = 0
        if i == 2:
            j = 0
            k = 1
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # our state (opponent's price)
        r_t_idx = np.where(prices == p_table[k, t-1])[0][0] # our other state (other opponent's price)
        
        maxedQ_idx = np.argmax(Q_table[r_t_idx, s_t_idx, :])
        return prices[maxedQ_idx]

#This set_price function is extended with the extra parameter r_next which it needs in order to pull the correct price
@njit
def set_price_ext(i, t, p_table, Q_table, prices, epsilon, r_next):
    
    if epsilon >= np.random.uniform(0,1):
        
        return np.random.choice(prices)
    else:
        if i == 0:
            j = 1
            k = 2
        if i == 1:
            j = 2
            k = 0
        if i == 2:
            j = 0
            k = 1
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # our state (opponent's price)
        r_t_idx = np.where(prices == r_next)[0][0]
        
        maxedQ_idx = np.argmax(Q_table[r_t_idx, s_t_idx, :])
        return prices[maxedQ_idx]
    

@njit
def Q(p_it_idx, s_t_idx, r_t_idx, i, t, alpha, delta, p_table, Q_table, prices, s_next, r_next) -> float: # p_table contains p and s (opponent price)
    if i == 0:
        j = 1
        k = 2
    if i == 1:
        j = 2
        k = 0
    if i == 2:
        j = 0
        k = 1

    prev_est = Q_table[r_t_idx, s_t_idx, p_it_idx]
    
    #s_next er s_{t+2} mens r_next er r_{t+1} som er blevet trukket fra set_price og set_price_ext. Disse skal bruges i new_est som estimater for hvilke priser firmaerne sætter i de næste perioder. 
    s_next_index = np.where(prices == s_next)[0][0] 
    r_next_index = np.where(prices == r_next)[0][0]
    #Den maksimale Q-værdi om til tidspunkt t+2 givet priserne som vi forventer virksomhederne sætter i denne periode. 
    maxed_Q = max(Q_table[r_next_index, s_next_index, :])
    
    
    
    new_est = profit(p_table[i, t], p_table[j, t], p_table[k, t]) + (delta * profit(p_table[i, t], s_next, p_table[k, t+1])+ delta**2 * profit(p_table[i, t], s_next, r_next))  + delta**3 * maxed_Q

    
    return (1 - alpha) * prev_est + alpha * new_est

@njit
def curr_prof(p_table, profits, i, t):
    if i == 0:
        j = 1
        k = 2
    if i == 1:
        j = 2
        k = 0
    if i == 2:
        j = 0
        k = 1
    profits[i, t] = profit(p_table[i,t], p_table[j,t], p_table[k,t])
    return


@njit
def bertrand_simulation(alpha, delta, T, prices):

    # array of possible prices firms can choose (in this case k=6)
    i = 0
    j = 1
    k = 2
    t = 0
    # calculate the decay parameter theta
    theta = -(1/1000000)**(1/T) + 1
    epsilon = (1 - theta)**t

    p = len(prices)
    Q_table1 = np.zeros((p, p, p)) # |P| x |S| matrix
    Q_table2 = np.zeros((p, p, p)) 
    Q_table3 = np.zeros((p, p, p)) 
    p_table = np.empty((3, T))
    p_table.fill(np.nan)
    profits = np.zeros((3, T))

    profitabilities0 = []
    profitabilities1 = []
    profitabilities2 = []
    
    p_table[i, :3] = np.random.choice(prices) # firm 0 sets price for periods t=0:2
    p_table[j, :3] = np.random.choice(prices) # firm 1 sets price for periods t=0:2
    p_table[k, :3] = np.random.choice(prices) # firm 2 sets price for periods t=0:2
    
    t = 3 # 3 periods have passed, so t = 3
    while t < T:

        if i == 0: # update firm 0
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            r_next = set_price(k, t, p_table, Q_table3, prices, epsilon)
            s_next = set_price_ext(j, t, p_table, Q_table2, prices, epsilon, r_next)
            Q_table1[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table1, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table1, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]
            

        if i ==1: # update firm 1
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            
            r_next = set_price(k, t, p_table, Q_table1, prices, epsilon)
            s_next = set_price_ext(j, t, p_table, Q_table3, prices, epsilon, r_next)
            Q_table2[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table2, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table2, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]


        if i ==2: # update firm 2
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            r_next = set_price(k, t, p_table, Q_table2, prices, epsilon)
            s_next = set_price_ext(j, t, p_table, Q_table1, prices, epsilon, r_next)
            Q_table3[r_t_idx, s_t_idx, p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table3, prices, r_next, s_next)
            
            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table3, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]

        
        # write profits for firm 0, 1 and 2
        curr_prof(p_table, profits, 0, t)
        curr_prof(p_table, profits, 1, t)
        curr_prof(p_table, profits, 2, t)
        
        if t % 12500 == 0:
            # compute avg. of last 1000 profits for each firm
            profitability0 = np.sum(profits[0, (t-1000):t])/1000 
            profitability1 = np.sum(profits[1, (t-1000):t])/1000
            profitability2 = np.sum(profits[2, (t-1000):t])/1000
            
            profitabilities0.append(profitability0)
            profitabilities1.append(profitability1)
            profitabilities2.append(profitability2)
            
        
        # calculate new epsilon using decay parameter
        epsilon = (1 - theta)**t
        # Update variables
        tmp = i
        i = j
        j = k
        k = tmp
        t += 1
    return p_table, profitabilities0, profitabilities1, profitabilities2
