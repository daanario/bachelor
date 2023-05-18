import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from numba import njit
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter

@njit
def demand(p1t, p2t):
    if (p1t < p2t):
        return 1 - p1t
    elif (p1t == p2t):
        return 0.5 * (1 - p1t)
    elif (p1t > p2t):
        return 0
    
@njit
def profit(p1t, p2t):
    return p1t * demand(p1t, p2t)

@njit
def Q(p_it_idx, s_t_idx, i, t, alpha, delta, p_table, Q_table, prices, s_next) -> float: # p_table contains p and s (opponent price)
    if i == 0:
        j = 1
    else:
        j = 0
    prev_est = Q_table[p_it_idx, s_t_idx]
    s_next_index=np.where(prices == s_next)[0][0] 
    maxed_Q = max(Q_table[:, s_next_index])
    new_est = profit(p_table[i, t], p_table[j, t]) + delta * profit(p_table[i, t], s_next) + delta**2 * maxed_Q
    return (1 - alpha) * prev_est + alpha * new_est

@njit
def set_price2(i, t, p_table, Q_table, prices, epsilon):
    if epsilon >= np.random.uniform(0,1):
        return np.random.choice(prices)
    else:
        if i == 0:
            j = 1
        else:
            j = 0
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # our state (opponent's price)
        maxedQ_idx = np.argmax(Q_table[:, s_t_idx])

        print("\nRow in Qtable in question\n",Q_table[:, s_t_idx])
        return prices[maxedQ_idx]
    
@njit
def set_price(i, t, p_table, Q_table, prices, epsilon):
    if epsilon >= np.random.uniform(0,1):
        return np.random.choice(prices)
    else:
        if i == 0:
            j = 1
        else:
            j = 0
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # our state (opponent's price)
        maxedQ_idx = np.argmax(Q_table[:, s_t_idx])

        return prices[maxedQ_idx]

@njit
def curr_prof(p_table, profits, i, t):
    if i == 0:
        j = 1
    else:
        j = 0
    profits[i, t] = profit(p_table[i,t], p_table[j,t])
    return 

@njit
def undercut(price, prices):
    if price > prices[0]: # if price is not lowest possible price
        price_idx = np.where(prices == price)[0][0]
        return prices[price_idx-1] # return price one index lower than opponent price
    else:
        return prices[0] # return lowest possible price
        

@njit
def bertrand_simulation(alpha, delta, T, prices):
    
    i = 0
    j = 1
    
    t = 0
    # calculate the decay parameter theta
    theta = -(1/1000000)**(1/T) + 1
    epsilon = (1 - theta)**t

    p = len(prices)
    Q_table1 = np.zeros((p, p)) # |P| x |S| matrix
    Q_table2 = np.zeros((p, p)) 

    p_table = np.zeros((2,T))
    profits = np.zeros((2,T))
    avg_profs1 = []
    avg_profs2 = []

    p_table[i, t] = np.random.choice(prices) # firm 1 sets price
    t += 1
    p_table[j, t] = np.random.choice(prices) # firm 2 sets price
    p_table[i, t] = p_table[i, t-1]
    t += 1 # now t = 2

    while t < T:

        if i == 0: # update firm 0
            # exploration module
            p_it_idx = np.where(prices == p_table[i, t-2])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-2])[0][0]
            s_next = set_price(j, t, p_table, Q_table2, prices, epsilon)
            Q_table1[p_it_idx, s_t_idx] = Q(p_it_idx, s_t_idx, i, t-2, alpha, delta, p_table, Q_table1, prices, s_next)
            
            
            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table1, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]



            # write profits for firm 0
            curr_prof(p_table, profits, 0, t)
            curr_prof(p_table, profits, 1, t)

            #compute avg profitability of last 1000 runs
            if t % 12500 == 0:
                profitability = np.sum(profits[i, (t-1000):t])/1000
                avg_profs1.append(profitability)
        else: # update firm 1
            # exploration module
            p_it_idx = np.where(prices == p_table[i, t-2])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-2])[0][0]
            s_next = set_price(j, t, p_table, Q_table1, prices, epsilon)
            Q_table2[p_it_idx, s_t_idx] = Q(p_it_idx, s_t_idx, i, t-2, alpha, delta, p_table, Q_table2, prices, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table2, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]

            # write profits for firm 1
            curr_prof(p_table, profits, 0, t)
            curr_prof(p_table, profits, 1, t)
            if t % 12500 == 1:    
                profitability = np.sum(profits[i, (t-1000):t])/1000
                avg_profs2.append(profitability)

        # calculate new epsilon using decay parameter
        epsilon = (1 - theta)**t

        tmp = i
        i = j
        j = tmp
        t += 1
    return p_table, avg_profs1, avg_profs2

@njit
def bertrand_simulation_forced_deviation(alpha, delta, T, prices):
    
    i = 0
    j = 1
    
    t = 0
    # calculate the decay parameter theta
    theta = -(1/1000000)**(1/T) + 1
    epsilon = (1 - theta)**t

    p = len(prices)
    Q_table1 = np.zeros((p, p)) # |P| x |S| matrix
    Q_table2 = np.zeros((p, p)) 

    p_table = np.zeros((2,T))
    profits = np.zeros((2,T))
    avg_profs1 = []
    avg_profs2 = []

    p_table[i, t] = np.random.choice(prices) # firm 1 sets price
    t += 1
    p_table[j, t] = np.random.choice(prices) # firm 2 sets price
    p_table[i, t] = p_table[i, t-1]
    t += 1 # now t = 2

    while t < T:

        if i == 0: # update firm 0
            # exploration module
            p_it_idx = np.where(prices == p_table[i, t-2])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-2])[0][0]
            s_next = set_price(j, t, p_table, Q_table2, prices, epsilon)
            Q_table1[p_it_idx, s_t_idx] = Q(p_it_idx, s_t_idx, i, t-2, alpha, delta, p_table, Q_table1, prices, s_next)
            
            
            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table1, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            
            if t == 499900: # force a deviation from collusive pricing
                #print("firm i is:", i)
                #print("firm j is:", j)
                #print("pre-deviation prices: \n p_0t:", p_table[0, t], "\n p_1t:", p_table[1, t ])
               
                p_table[i, t] = undercut(p_table[j, t], prices)
                #print("deviation price: ", p_table[i, t])
                
            # write profits for firm 0
            curr_prof(p_table, profits, 0, t)
            curr_prof(p_table, profits, 1, t)

            #compute avg profitability of last 1000 runs
            if t % 12500 == 0:
                profitability = np.sum(profits[i, (t-1000):t])/1000
                avg_profs1.append(profitability)
        else: # update firm 1
            # exploration module
            p_it_idx = np.where(prices == p_table[i, t-2])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-2])[0][0]
            s_next = set_price(j, t, p_table, Q_table1, prices, epsilon)
            Q_table2[p_it_idx, s_t_idx] = Q(p_it_idx, s_t_idx, i, t-2, alpha, delta, p_table, Q_table2, prices, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table2, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]

            # write profits for firm 1
            curr_prof(p_table, profits, 0, t)
            curr_prof(p_table, profits, 1, t)
            if t % 12500 == 1:    
                profitability = np.sum(profits[i, (t-1000):t])/1000
                avg_profs2.append(profitability)

        # calculate new epsilon using decay parameter
        epsilon = (1 - theta)**t

        tmp = i
        i = j
        j = tmp
        t += 1
    return p_table, avg_profs1, avg_profs2
