# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:55:45 2019

@author: Linh Pham Thi

This is a file to generate the random EV states
"""
import settings
from EVbattery import EVbattery
import numpy as np

def datagen():
    # Initializing variables
    evbatt = {}
    total_ev_demand = 0         # Total number of kWh of the batteries that need to 
                                # be filled
    total_inst_chargerate = 0   # The number of kW needed at the moment that - if
                                # sustained constantly, will change the cars fully
                                # by the time they leaves
                                
    # Iterating to generate the EV battery attributes
    for n in range(1,(settings.carnumber+1)):
            
            capacity = np.random.gamma(5.66,7)
            SOC = np.random.beta(2,1.7)
            time = np.random.normal(10,2.1)
            
            if time > 4:
                ctype = 0 #slow charging takes 8 hours to charge from flat to full
            else:
                ctype = 1 #fast charging takes 4 hours to charge from flat to full
            
            evbatt["EV{0}".format(n)]=EVbattery(capacity,SOC,time,ctype)
            total_ev_demand = total_ev_demand + evbatt["EV{0}".format(n)].fill
            total_inst_chargerate = total_inst_chargerate + evbatt["EV{0}".format(n)].avg_chargerate
            
    return evbatt, total_ev_demand, total_inst_chargerate