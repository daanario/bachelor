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
def demand(p0t, p1t, p2t):
    if (p0t < p1t) and (p0t<p2t):
        return 1 - p0t
    elif (p0t == p1t == p2t):
        return 1/3 * (1 - p0t)
    elif (p0t > p1t) or (p0t > p2t):
        return 0
    elif ((p0t < p1t) and (p0t == p2t)) or ((p0t == p1t) and (p0t < p2t)):
        return 1/2 * (1 - p0t)
    
@njit
def profit(p0t, p1t, p2t):
    return p0t * demand(p0t, p1t, p2t)
    
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
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # last price by firm j (trailing by 2 periods)
        r_t_idx = np.where(prices == p_table[k, t-1])[0][0] # last price by firm k (just set last period)
        
        maxedQ_idx = np.argmax(Q_table[r_t_idx, s_t_idx, :]) # r_t_idx is the price set before i, s_t_idx is the last price of the firm that is setting the price next round
        return prices[maxedQ_idx]

@njit
def guess_s(i, t, p_table, Q_table, prices, epsilon):
    
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
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # last price by firm j (trailing by 2 periods)
        r_t_idx = np.where(prices == p_table[k, t-1])[0][0] # last price by firm k (just set last period)
        
        maxedQ_idx = np.argmax(Q_table[r_t_idx, s_t_idx, :]) # r_t_idx is the price set before i, s_t_idx is the last price of the firm that is setting the price next round
        return prices[maxedQ_idx]

#This set_price function is extended with the extra parameter r_next which it needs in order to pull the correct price
@njit
def guess_r(i, t, p_table, Q_table, prices, epsilon, s_next):
    
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
        r_t_idx = np.where(prices == s_next)[0][0] # firm k just set this price
        s_t_idx = np.where(prices == p_table[j, t-1])[0][0] # firm j is still locked since 2 rounds ago
        
        
        maxedQ_idx = np.argmax(Q_table[r_t_idx, s_t_idx, :]) # r_t_idx is the price set before i, s_t_idx is the last price of the firm that is setting the price next round
        return prices[maxedQ_idx]
    

@njit
def Q(p_it_idx, s_t_idx, r_t_idx, i, t, alpha, delta, p_table, Q_table, prices, r_next, s_next) -> float: # p_table contains p and s (opponent price)
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
    
    
    
    new_est = profit(p_table[i, t], p_table[j, t], p_table[k, t]) + (delta * profit(p_table[i, t], s_next, p_table[k, t])+ delta**2 * profit(p_table[i, t], s_next, r_next))  + delta**3 * maxed_Q

    

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
    Q_table0 = np.zeros((p, p, p)) # |P| x |S| matrix
    Q_table1 = np.zeros((p, p, p)) 
    Q_table2 = np.zeros((p, p, p)) 
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
            s_next = guess_s(j, t, p_table, Q_table1, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table2, prices, epsilon, s_next)
            Q_table0[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table0, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table0, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]
            

        if i ==1: # update firm 1
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            
            s_next = guess_s(j, t, p_table, Q_table2, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table0, prices, epsilon, s_next)
            Q_table1[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table1, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table1, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]


        if i ==2: # update firm 2
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            s_next = guess_s(j, t, p_table, Q_table0, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table1, prices, epsilon, s_next)
            Q_table2[r_t_idx, s_t_idx, p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table2, prices, r_next, s_next)
            
            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table2, prices, epsilon)
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
























@njit
def undercut(price1, price2, prices):
    price = min(price1, price2)
    
    if price > prices[0]: # if price is not lowest possible price
        price_idx = np.where(prices == price)[0][0]
        return prices[price_idx-1] # return price one index lower than opponent price
    else:
        return prices[0] # return lowest possible price
    
@njit
def bertrand_simulation_forced_deviation(alpha, delta, T, prices):

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
            
            if t == 499899: # force a deviation from collusive pricing
                #print("firm i is:", i)
                #print("firm j is:", j)
                #print("firm k is:", k)
                #print("pre-deviation prices: \n p_0t:", p_table[0, t], "\n p_1t:", p_table[1, t ], "\n p_2t:", p_table[2,t])
               
                p_table[i, t] = undercut(p_table[j, t], p_table[k, t], prices)
                #print("deviation price: ", p_table[i, t])

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
#@njit. Doesnt work when jitted, could be solved but I didn't bother so don't jit this function
def bertrand_simulation_convergence(alpha, delta, T, prices):

    # array of possible prices firms can choose (in this case k=6)
    i = 0
    j = 1
    k = 2
    t = 0

    # calculate the decay parameter theta
    theta = -(1/1000000)**(1/T) + 1
    epsilon = (1 - theta)**t

    p = len(prices)
    Q_table0 = np.zeros((p, p, p)) # |P| x |S| matrix
    Q_table1 = np.zeros((p, p, p)) 
    Q_table2 = np.zeros((p, p, p)) 
    p_table = np.empty((3, T))
    p_table.fill(np.nan)
    profits = np.zeros((3, T))

    # convergence plot arrays and variables
    Q_norm_array0 = []
    Q_norm_array1 = []
    Q_norm_array2 = []
    toggle =0
    counter = 0
    
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
            s_next = guess_s(j, t, p_table, Q_table1, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table2, prices, epsilon, s_next)
            Q_table0[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table0, prices, r_next, s_next)

            # action module 
            p_table[i, t] = set_price(i, t, p_table, Q_table0, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]

            

        if i ==1: # update firm 1
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            
            s_next = guess_s(j, t, p_table, Q_table2, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table0, prices, epsilon, s_next)
            Q_table1[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table1, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table1, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]


        if i ==2: # update firm 2
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            s_next = guess_s(j, t, p_table, Q_table0, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table1, prices, epsilon, s_next)
            Q_table2[r_t_idx, s_t_idx, p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table2, prices, r_next, s_next)
            
            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table2, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]

        
        # write profits for firm 0, 1 and 2
        curr_prof(p_table, profits, 0, t)
        curr_prof(p_table, profits, 1, t)
        curr_prof(p_table, profits, 2, t)
        #makes sure that we get Q_table_t and Q_table_{t+1} for each player
        if toggle == True:
            counter+=1
        # Calculating convergence every 1000 iteration
        if t % 1000 == 0:
            # Save Q_matrices
            Q_table0_old=np.copy(Q_table0)
            Q_table1_old=np.copy(Q_table1)
            Q_table2_old=np.copy(Q_table2)

            toggle = True
        if counter ==3:
            
            # Calculate the difference between Q_table0 and Q_table1
            difference0 = Q_table0-Q_table0_old
            difference1 = Q_table1-Q_table1_old
            difference2 = Q_table2-Q_table2_old

            # Find the norms
            norm0 = np.linalg.norm(difference0)
            norm1=np.linalg.norm(difference1)
            norm2=np.linalg.norm(difference2)


            # Append to norm array
            Q_norm_array0.append(norm0)
            Q_norm_array1.append(norm1)
            Q_norm_array2.append(norm2)

            toggle = False
            counter =0

        
            
        
        # calculate new epsilon using decay parameter
        epsilon = (1 - theta)**t
        # Update variables
        tmp = i
        i = j
        j = k
        k = tmp
        t += 1
    return p_table, Q_norm_array0, Q_norm_array1, Q_norm_array2

@njit
def bertrand_simulation_theta(alpha, delta, T, theta, prices):
    i = 0
    j = 1
    k = 2
    t = 0

    epsilon = (1 - theta)**t

    p = len(prices)
    Q_table0 = np.zeros((p, p, p)) # |P| x |S| matrix
    Q_table1 = np.zeros((p, p, p)) 
    Q_table2 = np.zeros((p, p, p)) 
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
            s_next = guess_s(j, t, p_table, Q_table1, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table2, prices, epsilon, s_next)
            Q_table0[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table0, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table0, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]
            

        if i ==1: # update firm 1
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            
            s_next = guess_s(j, t, p_table, Q_table2, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table0, prices, epsilon, s_next)
            Q_table1[r_t_idx, s_t_idx,p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table1, prices, r_next, s_next)

            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table1, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]


        if i ==2: # update firm 2
            # learning module
            p_it_idx = np.where(prices == p_table[i, t-3])[0][0]
            s_t_idx =  np.where(prices == p_table[j, t-3])[0][0]
            r_t_idx =  np.where(prices == p_table[k, t-3])[0][0]
            s_next = guess_s(j, t, p_table, Q_table0, prices, epsilon)
            r_next = guess_r(k, t, p_table, Q_table1, prices, epsilon, s_next)
            Q_table2[r_t_idx, s_t_idx, p_it_idx] = Q(p_it_idx, s_t_idx,r_t_idx, i, t-3, alpha, delta, p_table, Q_table2, prices, r_next, s_next)
            
            # action module
            p_table[i, t] = set_price(i, t, p_table, Q_table2, prices, epsilon)
            p_table[j, t] = p_table[j, t-1]
            p_table[k, t] = p_table[k, t-1]

        
        # write profits for firm 0, 1 and 2
        curr_prof(p_table, profits, 0, t)
        curr_prof(p_table, profits, 1, t)
        curr_prof(p_table, profits, 2, t)
        
        if t % 1000 == 0:
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