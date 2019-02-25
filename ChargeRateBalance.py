# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:41:41 2019

@author: Linh Pham Thi

This file contains the function to balance the charging rates among the charging cars.
"""
import settings
import numpy as np

def ChargeRateBalance(evbatt,pv_leftover_energy):
    # =========================================================================
    # Initialising variables
    # =========================================================================
    pv_energy_available = settings.pv_energy_profile[settings.hour]
    
    for n in range(1,settings.carnumber+1):
        evbatt["EV{0}".format(n)].chargerate = 0

    # =========================================================================
    # Determining chargegrates
    # =========================================================================

    while pv_energy_available > 0:
        total_weigh = 0
 
        # =====================================================================
        # Terms for the weighted average
        # =====================================================================     
        for n in range(1,settings.carnumber+1):
            
            # If the charging port is already at its limit, give no weight, otherwise use parameters to determine weighting
            if evbatt["EV{0}".format(n)].arrivaltime < settings.current_datetime: # No charging before the car has arrived
                evbatt["EV{0}".format(n)].rel_weigh = 0
            elif (evbatt["EV{0}".format(n)].chargetype == 0 and evbatt["EV{0}".format(n)].chargerate == settings.slowcharge_ulim) \
                    or (evbatt["EV{0}".format(n)].chargetype == 1 and evbatt["EV{0}".format(n)].chargerate == settings.fastcharge_ulim):
                evbatt["EV{0}".format(n)].rel_weigh = 0
            else:
                evbatt["EV{0}".format(n)].rel_weigh = evbatt["EV{0}".format(n)].fill / evbatt["EV{0}".format(n)].time
            
            total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh

        # =====================================================================
        # Break out of the while loop if all of the charging ports are at their limit
        # =====================================================================         
        if total_weigh == 0 :
            # Integrate leftover PV energy during the day by using trapezoidal rule
            pv_leftover_energy += pv_energy_available * settings.t_inc              
            break
            
        # =====================================================================
        # Calculating charging rates
        # =====================================================================  
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
  
    # Reset chargerate to zero if SOC is 1
    for n in range(1,settings.carnumber+1):
        if evbatt["EV{0}".format(n)].SOC >= 1:
            evbatt["EV{0}".format(n)].chargerate = 0
        
    return evbatt, pv_energy_available, pv_leftover_energy