# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:02:56 2019

@author: Linh Pham Thi

This function calculates the energy we have to buy from the grid based on the 
predicted PV output for the rest of the day.
"""
import settings
import numpy as np


def gridEnergyCalculator(evbatt, grid_energy_needed):
    for n in range(1,settings.carnumber+1):
        
        # Picking out the EVs that after the energy division are charging at a sub-optimal rate
       
        if evbatt["EV{0}".format(n)].chargetype == 0 and \
           (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim)) and \
           (evbatt["EV{0}".format(n)].SOC < 1):       #Slow charge
            grid_energy_needed += np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim) - evbatt["EV{0}".format(n)].chargerate
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim)
        elif evbatt["EV{0}".format(n)].chargetype == 1 and \
             (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim)) and \
             (evbatt["EV{0}".format(n)].SOC < 1):       #Fast charge: 
            grid_energy_needed += np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim) - evbatt["EV{0}".format(n)].chargerate
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim)
                
    return evbatt, grid_energy_needed