# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 23:34:37 2022

@author: wolfeli
"""


import numpy as np
from scipy.optimize import minimize


def adj1s_hpfilter(y, lm_2 = 1600, opt = False):

    
    '''

    Code for "On adjusting the one-sided Hodrick-Prescott filter" (2020) 
    by Elias Wolf (FU-Berlin), Frieder Mokinski (Deutsche Bundesbank), and
    Yves Schüler (Deutsche Bundesbank)
    
    Version date 2022/03/2
    If you encounter any bug, please mail Elias Wolf at e.wolf@fu-berlin.de
    
    This program estimates the cyclical component of the adjusted one-sided HP
    filter (HP-1s*) by estimating the two-sided HP filter (HP-2s) 
    on an expanding sample and keeping the last observation.
    
    For the exact references that are cited in this program, please see
    the paper.
    
          Input:    
                     y       - a Tx1 vector (y_1,...,y_T)', where T is the
                     number of observations. 
                         
                     lm_2  - a scalar. This is the value of the smoothing
                     parameter usually employed for the two-sided HP filter
                     (HP2s). This input is optional. The default is lm_2=1,600.

                     opt    - boolean. If opt=True, the adjustment parameters are
                     obtained through the optimization routine (computationally more intensive).
                     This input is optional. The default is opt=0 (computationally less intensive).
    
        Output:  
                     ycycle_adj  - a Tx1 array with the adjusted extracted cyclical component
                
                     lm_1        - a scalar. This is the adjusted value of the smoothing parameter used as an input to the one-sided HP filter
    
                     kappa       - a scalar. This is the mulitplicative scaling factor, with wich the cyclical component of the
                     one-sided HP filter is rescaled
    
       Example:
                     ycycle_adj, lm1, kappa=adj1s_hpfilter(y,1600)
                     yields a Tx1 array of the extracted cyclical component
                     using a smoothing parameter of 650 and scaling
                     parameter of size 1.1513 for the one-sided HP filter                 

    '''

    
    if len(y) == 0:

        raise Exception('Time series is missing or empty')

    if lm_2 == 1600 and opt == True:

        print('Warning: Smoothing parameter not privided. Smoothing parameter is set to 1,600')

    if np.isnan(np.sum(y)) == True:

        raise Exception('y contains missing values: please remove')

    if len(y.shape) > 1:

        raise Exception('y contains more than one time series: the program is designed for one series only')

    if y.shape[0] < 3:

        raise Exception('y contains less than 3 observations: please check your data input')

    
    '''

    polynomials providing lm_1 and kappa designed for values of lm_2 in
    the range of [6.25:1000000]. Polynomials fitted on the basis of
    values given in Table 2 in Appendix A

    '''


    def poly_lm(lm_2):  

        lm_1 = -5.071743 +  0.4080780*lm_2  -0.749537*lm_2**(1/2) + 14.50001*lm_2**(1/3) -50.36123*lm_2**(1/4) + 41.44369*lm_2**(1/5)

        return(lm_1)

    
    def poly_kappa(lm_2):

        kappa = 0.984928 +  0.547209*(1/lm_2)  - 0.703636*(1/np.sqrt(lm_2)) + 3.291657*(1/(lm_2)**(1/3)) - 3.165415*(1/(lm_2)**(1/4)) + 1.759527 *(1/(lm_2)**(1/5))

        return(kappa)

        
    if opt == False:

        lm_1 = poly_lm(lm_2)
        kappa = poly_kappa(lm_2)

    if opt == True:

        '''
        
        Define cost function for optimization routine calculating the squared
        distance between the PTF of the two sided and the one sided HP-Filter.
        For the PTF of the one-sided filter, the weights are calculated based 
        on the formula given by Hamilton (2018) and subsequnetly cast into the 
        fequency domain using the FFT. The PTF of the two-sided filter is 
        constructed using the closed form solution for large samples 
        given by King and Rebello (1993). To avoid problems related to small 
        sample sizes we use a sample size of T=1000.

        ''' 

        def ptf_cost(params, lm_2):

            # Parameters to be optimized
            lm_1 = params[0]
            ratio = params[1]

            # Weights of the one-sided HP-filter
            T = 1000

            I = np.eye(T)
            Q = np.diff(I,2)
            A_inv = np.linalg.inv(I + lm_1*np.dot(Q.T, Q)) 
            wts_one = A_inv[-1,:]

            
            # FFT of the weigths to obtain PTF of the one-side HP-filter
            grid = 2*np.pi*np.asarray(range(int(np.floor(T/2))+1))/T

            k = np.asarray(range(-(T-1), 1))
            k = np.transpose(k)
            hpgain = []

            for i in range(1, len(grid)+1):

                hpgain.append(1 - np.ones(shape=(1, len(k))).dot(wts_one.T*np.exp(1j*grid[i-1]*k)))

            hp1_ptf = np.concatenate(np.abs(hpgain)**2)

            # PTF of the two-sided HP_filter 
            hp2_ptf = ((4*lm_2*(1-np.cos(grid))**2/(1+4*lm_2*(1-np.cos(grid))**2))**2)

            # Calculate loss function defined as the squared distance    
            cost = sum((ratio*hp1_ptf-hp2_ptf)**2)

            return(cost)


        # Initial vlaues and optimizationof teh cost function
        init_vals = np.asarray([poly_lm(lm_2), poly_kappa(lm_2)])
        res = minimize(ptf_cost, init_vals, args=lm_2, method='BFGS',
                       options={'disp': True})


        # Collect optimal parameters
        lm_1 = res.x[0]
        kappa = np.sqrt(res.x[1])


    '''
    
    Function for the one-sided HP-Filter to calculate the cyclical component
    based on the weights given by Proposition 1

    '''
    def hp_one(lm_1, kappa, y):

        y = np.asarray(y)
        T_series =  len(y)
        cycle_os = []

        for i in range(3,T_series+1):
            
            I = np.eye(i)
            Q = np.diff(I,2)
            A_inv = np.linalg.inv(I + lm_1*np.dot(Q.T, Q)) 
            
            psi_t = y[i] - A_inv[-1,:].dot(y[:i])
            cycle_os.append(psi_t)

        return(kappa*np.asarray(cycle_os))


    # Apply the one-sided HP-Filter to the series
    ycycle_adj = hp_one(lm_1, kappa, y)

    return([ycycle_adj, lm_1, kappa])