# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

This file contains all the global variables and all variables that need to be
initialized or tuned for the simulation
"""
import datetime
from pvAsset import PVasset

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
base=14.7
red_energy_cost = (base + 5.363)/100         # Base rate + DUOS charge           
amber_energy_cost = (base + 0.57)/100
green_energy_cost = (base + 0.452)/100


""" PV related (Nicole's code)"""
# Fixed values
pv_area = 1.956 * 0.992   # Area of one panel        
 
# Variable parameters

dt = 60/60              # Time period (hr)
pv_efficiency = 1    # Efficiency of one panel (max 0.18, degrades with time)
pv_losses = 0.14        # Losses from wires/inverters/etc; 0.14 recommended by PVGIS
num_pv_bays=10
pv_number = num_pv_bays*15        # Total number of panels (max 4995, given 15 panels per 3-bay unit, 1000 bays total) 

# Generating an instance 
pv_capacity = pv_efficiency * pv_area #at max efficiency this is 0.35kW as manufacturer states
pv_site1 = PVasset(pv_capacity * pv_number * (1 - pv_losses))
