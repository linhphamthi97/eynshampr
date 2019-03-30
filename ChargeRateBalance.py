# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:41:41 2019

@author: Linh Pham Thi

This file contains the function to balance the charging rates among the charging cars.
"""
import settings
import numpy as np
import sys
import showResults as sr

def chargeRateBalance (evbatt, simulation):
    # =========================================================================
    # Initialising variables
    # =========================================================================
    pv_energy_profile = np.loadtxt('total_' + str(simulation.current_datetime.month) + '_kWh.txt')
    
    pv_energy_available = pv_energy_profile[simulation.current_hour]
    
    for n in range (1, settings.vnumber + 1):
        evbatt["EV{0}".format(n)].chargerate = 0

    # =========================================================================
    # Determining chargegrates
    # =========================================================================

    # Reset chargerate to zero if SOC is 1 or car left the site
    for n in range (1, settings.vnumber + 1):
        if evbatt["EV{0}".format(n)].SOC >= 1 or evbatt["EV{0}".format(n)].present == 0:
            evbatt["EV{0}".format(n)].chargerate = 0
            evbatt["EV{0}".format(n)].rel_weigh = 0


    while pv_energy_available > 0:
        total_weigh = 0
        # =====================================================================
        # Terms for the weighted average
        # =====================================================================     
        for n in range (1, settings.vnumber + 1):
            
            # If the charging port is already at its limit, give no weight, otherwise use parameters to determine weighting
            if evbatt["EV{0}".format(n)].chargerate == evbatt["EV{0}".format(n)].crlimit:
                evbatt["EV{0}".format(n)].rel_weigh = 0
            else:
                evbatt["EV{0}".format(n)].rel_weigh = evbatt["EV{0}".format(n)].fill / evbatt["EV{0}".format(n)].time

            # Set chargerate to zero if SOC is 1 or if car is not present at the site
            if evbatt["EV{0}".format(n)].SOC >= 1 or evbatt["EV{0}".format(n)].present == 0:
                evbatt["EV{0}".format(n)].chargerate = 0
                evbatt["EV{0}".format(n)].rel_weigh = 0

        x = 0
        y = 0
        for n in range (1, settings.vnumber + 1):
            if evbatt["EV{0}".format(n)].present == 1 and evbatt["EV{0}".format(n)].need_maxcharge == 1\
               and evbatt["EV{0}".format(n)].SOC < 1:
                x += evbatt["EV{0}".format(n)].crlimit

            
        if x <= settings.priority_limit * pv_energy_profile[simulation.current_hour]:
            if evbatt["EV{0}".format(n)].present == 1 and evbatt["EV{0}".format(n)].need_maxcharge == 1\
               and evbatt["EV{0}".format(n)].SOC < 1:
                evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].crlimit
                evbatt["EV{0}".format(n)].rel_weigh = 0
            
        for n in range (1, settings.vnumber + 1):
            y += evbatt["EV{0}".format(n)].chargerate
            total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh
            
        pv_energy_available = pv_energy_profile[simulation.current_hour] - y                

        total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh
            
            
        # =====================================================================
        # Break out of the while loop if all of the charging ports can't be charging or is at their limit
        # =====================================================================         
        if total_weigh == 0 :
            # Integrate leftover PV energy during the day by using trapezoidal rule
            sr.pv_leftover_energy += pv_energy_available * simulation.t_inc 

            pv_energy_available = pv_energy_profile[simulation.current_hour]
            for n in range (1, settings.vnumber + 1):
                pv_energy_available = pv_energy_available - evbatt["EV{0}".format(n)].chargerate            
            
            break
            
        # =====================================================================
        # Calculating charging rates
        # =====================================================================  
        for n in range (1, settings.vnumber + 1):
            # Calculating the chargerate with the weighted division on energy available
            evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].chargerate + (pv_energy_available * evbatt["EV{0}".format(n)].rel_weigh / total_weigh)
            
            # Implement restrictions on charging rates imposed by charging type
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate, 0, evbatt["EV{0}".format(n)].crlimit)

            

        # =====================================================================
        # Calculating leftover energy after the clip
        # =====================================================================  
        total_chargerate = 0
        for n in range (1, settings.vnumber + 1):
            total_chargerate += evbatt["EV{0}".format(n)].chargerate
        
        pv_energy_available = pv_energy_profile[simulation.current_hour] - total_chargerate
        
        # For debugging
        if pv_energy_available < -0.01:  # Ideally zero, but it sometimes goes negative by a very small amount (order of e-15) due to rounding errors
            print('PLease run the simulation again. BUG')
            sys.exit()
 
    # For plotting unused PV energy
    sr.unused_pv_energy.append(pv_energy_available)
    sr.unused_pv_energy_day += pv_energy_available
       
    return evbatt