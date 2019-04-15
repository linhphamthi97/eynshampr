# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

This file contains all the global variables and all variables that need to be
initialized or tuned for the simulation
"""
from fix import capacity
import datetime
from pvAsset import PVasset
import numpy as np
import sys
import showResults as sr

# =============================================================================
# Variables to change
# =============================================================================
""" Car and charging related """
slowcharge_ulim = 3         # kW charging upper limit
fastcharge_ulim = 7         # kW charging upper limit
rapidcharge_ulim = 50       # kW charging upper limit

end_SOC_req = 0.8           # The achievable SOC at leaving below which car is given charging priority
priority_limit = 0.8        

carnumber = 66              # cars/day

buschargelength = 0.25      # hour of charging for 1 bus
busnumber = 17              # bus / day, 17 corresponds to 1 bus/hour

vnumber = carnumber + busnumber     # Number of vehicles

""" Simulation related """
starttime = datetime.datetime(2020,1,1,6,0,0)        # Selected date for simulation, start time of simulation
endtime = datetime.datetime(2020,12,31,23,0)         # End time of simulation
time_increment = 24                              # [hours]


""" P&R operation related """
opentime = 6        # Opening time, hour
closetime = 23      # Closing time, hour
           

""" Finance related """
# Price of electricity, GPB per kWh
base=0.147
red_energy_cost = (base + 5.363)/100         # Base rate + DUOS charge           
amber_energy_cost = (base + 0.57)/100
green_energy_cost = (base + 0.452)/100


""" PV related (Nicole's code)"""
# Fixed values
pv_area = 1.956 * 0.992   # Area of one panel        
 
# Variable parameters

dt = 60/60              # Time period (hr)
pv_efficiency = 0.17    # Efficiency of one panel (max 0.18, degrades with time)
pv_losses = 0.14        # Losses from wires/inverters/etc; 0.14 recommended by PVGIS
num_pv_bays=10
pv_number = num_pv_bays*15        # Total number of panels (max 4995, given 15 panels per 3-bay unit, 1000 bays total) 

# Generating an instance 
#pv_capacity = pv_efficiency * pv_area #at max efficiency this is 0.35kW as manufacturer states
pv_capacity= capacity
pv_site1 = PVasset(pv_capacity * pv_number * (1 - pv_losses))




#///////////////////////////////////////////////////////////////////
#from ChargeRateBalance.py
def chargeRateBalance (evbatt, simulation, solar_profile):
    # =========================================================================
    # Initialising variables
    # =========================================================================
    pv_energy_profile = solar_profile[simulation.PVrange_begin : simulation.PVrange_end]
    
    pv_energy_available = pv_energy_profile[simulation.current_hour]
    
    for n in range (1, vnumber + 1):
        evbatt["EV{0}".format(n)].chargerate = 0

    # =========================================================================
    # Determining chargegrates
    # =========================================================================

    # Reset chargerate to zero if SOC is 1 or car left the site
    for n in range (1, vnumber + 1):
        if evbatt["EV{0}".format(n)].SOC >= 1 or evbatt["EV{0}".format(n)].present == 0:
            evbatt["EV{0}".format(n)].chargerate = 0
            evbatt["EV{0}".format(n)].rel_weigh = 0


    while pv_energy_available > 0:
        total_weigh = 0
        # =====================================================================
        # Terms for the weighted average
        # =====================================================================     
        for n in range (1, vnumber + 1):
            
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
        for n in range (1, vnumber + 1):
            if evbatt["EV{0}".format(n)].present == 1 and evbatt["EV{0}".format(n)].need_maxcharge == 1\
               and evbatt["EV{0}".format(n)].SOC < 1:
                x += evbatt["EV{0}".format(n)].crlimit

            
        if x <= priority_limit * pv_energy_profile[simulation.current_hour]:
            if evbatt["EV{0}".format(n)].present == 1 and evbatt["EV{0}".format(n)].need_maxcharge == 1\
               and evbatt["EV{0}".format(n)].SOC < 1:
                evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].crlimit
                evbatt["EV{0}".format(n)].rel_weigh = 0
            
        for n in range (1, vnumber + 1):
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
            for n in range (1, vnumber + 1):
                pv_energy_available = pv_energy_available - evbatt["EV{0}".format(n)].chargerate            
            
            break
            
        # =====================================================================
        # Calculating charging rates
        # =====================================================================  
        for n in range (1, vnumber + 1):
            # Calculating the chargerate with the weighted division on energy available
            evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].chargerate + (pv_energy_available * evbatt["EV{0}".format(n)].rel_weigh / total_weigh)
            
            # Implement restrictions on charging rates imposed by charging type
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate, 0, evbatt["EV{0}".format(n)].crlimit)

            

        # =====================================================================
        # Calculating leftover energy after the clip
        # =====================================================================  
        total_chargerate = 0
        for n in range (1, vnumber + 1):
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