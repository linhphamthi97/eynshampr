# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:41:41 2019

@author: Linh Pham Thi

This file contains the function to balance the charging rates among the charging cars
Inputs: EV battery, settings and datagen variables
Output: Sum of all the chargerates
"""
import settings
import EVbattery
from datagen import evbatt as evbatt

def ChargeRateBalance():
    # Initialising variables
    total_weigh = 0
    total_chargerate = 0
    
    # Terms for the weighted average
    for n in range(1,settings.carnumber+1):
        evbatt["EV{0}".format(n)].rel_weigh = evbatt["EV{0}".format(n)].fill / evbatt["EV{0}".format(n)].time
        total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh
    
    # Calculating chargerate for each car and charge
    for n in range(1,settings.carnumber+1):
        print('EV',n, 'SOC before charging: ',evbatt["EV{0}".format(n)].SOC)
        
        chargerate = settings.pv_energy_profile[settings.hour] * evbatt["EV{0}".format(n)].rel_weigh / total_weigh
        total_chargerate = total_chargerate + chargerate
        return total_chargerate
        
        # Charging
        evbatt["EV{0}".format(n)].charge(chargerate,settings.t_inc)
        
        print('EV',n, 'Chargerate: ', chargerate)
        print('EV',n, 'SOC after charging: ',evbatt["EV{0}".format(n)].SOC)
        print('')