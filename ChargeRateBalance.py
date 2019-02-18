# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:41:41 2019

@author: Linh Pham Thi

This file contains the function to balance the charging rates among the charging cars.
Inputs: EV battery, settings and datagen variables
Output: Sum of all the chargerates
"""
import settings
import numpy as np
import matplotlib.pyplot as plt

def ChargeRateBalance(evbatt):
    # =========================================================================
    # Initialising variables
    # =========================================================================
    total_chargerate = 0
    SOC_plot=list()
    pv_energy_available = settings.pv_energy_profile[settings.hour]
    
    for n in range(1,settings.carnumber+1):
        evbatt["EV{0}".format(n)].chargerate = 0

    # =========================================================================
    # Determining chargegrates
    # =========================================================================
    
    # Calculating chargerate for each car and charge
    while pv_energy_available > 0:
        total_weigh = 0
        
        # Terms for the weighted average
        for n in range(1,settings.carnumber+1):
            
            # If the charging port is already at its limit, give no weight, otherwise use parameters to determine weighting
            if (evbatt["EV{0}".format(n)].chargetype == 0 and evbatt["EV{0}".format(n)].chargerate == settings.slowcharge_ulim) \
                    or (evbatt["EV{0}".format(n)].chargetype == 1 and evbatt["EV{0}".format(n)].chargerate == settings.fastcharge_ulim):
                evbatt["EV{0}".format(n)].rel_weigh = 0
            else:
                evbatt["EV{0}".format(n)].rel_weigh = evbatt["EV{0}".format(n)].fill / evbatt["EV{0}".format(n)].time
            
            total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh
        
        # Break out of the while loop if all of the charging ports are at their limit
        if total_weigh == 0 :
            break
            
        for n in range(1,settings.carnumber+1):
            # Calculating the chargerate with the weighted division on energy available
            evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].chargerate + (pv_energy_available * evbatt["EV{0}".format(n)].rel_weigh / total_weigh)
            
            # Implement restrictions on charging rates imposed by charging type
            if evbatt["EV{0}".format(n)].chargetype == 0:       #Slow charge
                evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate,0,settings.slowcharge_ulim)
            else: 
                evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate,0,settings.fastcharge_ulim)
            
            
        pv_energy_available = settings.pv_energy_profile[settings.hour]
        
        for n in range(1,settings.carnumber+1):
            pv_energy_available = pv_energy_available - evbatt["EV{0}".format(n)].chargerate
                     
    # =========================================================================
    # Charging and plotting results
    # =========================================================================
    for n in range(1,settings.carnumber+1):
        print('EV',n, 'SOC before charging: ',evbatt["EV{0}".format(n)].SOC)
        
        total_chargerate += evbatt["EV{0}".format(n)].chargerate
               
        evbatt["EV{0}".format(n)].charge(evbatt["EV{0}".format(n)].chargerate,settings.t_inc)
       
        print('EV',n, 'Chargerate: ', evbatt["EV{0}".format(n)].chargerate)
        print('EV',n, 'SOC after charging: ',evbatt["EV{0}".format(n)].SOC)
        print('')
               
        # For plotting
        SOC_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
        
    print('Leftover energy: ', np.clip(pv_energy_available, 0, None), ' kW')
    
    # Plotting a graph of the SOC
    y_axis = np.arange(len(SOC_plot)) 
    plt.barh(y_axis, SOC_plot)
    plt.title('State of charge of the EVs')
    plt.xlabel('State of charge [%]')
    plt.show()
      
    
    return evbatt, total_chargerate