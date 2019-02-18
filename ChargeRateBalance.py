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
    # Initialising variables
    total_weigh = 0
    total_chargerate = 0
    pv_energy_available = settings.pv_energy_profile[settings.hour]
    SOC_plot=list()
#    extra_charging=list()
    
    
    # Calculating chargerate for each car and charge
    for n in range(1,settings.carnumber+1):
        print('EV',n, 'SOC before charging: ',evbatt["EV{0}".format(n)].SOC)
        
        # Terms for the weighted average
        for k in range(n,settings.carnumber+1):
            evbatt["EV{0}".format(k)].rel_weigh = evbatt["EV{0}".format(k)].fill / evbatt["EV{0}".format(k)].time
            total_weigh = total_weigh + evbatt["EV{0}".format(k)].rel_weigh       
        
        evbatt["EV{0}".format(n)].chargerate = pv_energy_available * evbatt["EV{0}".format(n)].rel_weigh / total_weigh
        
        # Implement restrictions on charging rates imposed by charging type
        if evbatt["EV{0}".format(n)].chargetype == 0:       #Slow charge
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate,0,settings.slowcharge_ulim)
        else: 
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate,0,settings.fastcharge_ulim)
        
        # Total energy left
        pv_energy_available = pv_energy_available - evbatt["EV{0}".format(n)].chargerate
        
                 
        # Charging
        evbatt["EV{0}".format(n)].charge(evbatt["EV{0}".format(n)].chargerate,settings.t_inc)
        
        print('EV',n, 'Chargerate: ', evbatt["EV{0}".format(n)].chargerate)
        print('EV',n, 'SOC after charging: ',evbatt["EV{0}".format(n)].SOC)
        print('')
        
        # For plotting
        SOC_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
        
 
    print('Leftover energy: ', pv_energy_available, ' kWh')
    
    # Plotting a graph of the SOC
    y_axis = np.arange(len(SOC_plot)) 
    plt.barh(y_axis, SOC_plot)
    plt.title('State of charge of the EVs')
    plt.xlabel('State of charge [%]')
    plt.show()
      
    
    return evbatt, total_chargerate