# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

This file contains all the global variables and all variables that need to be
initialized or tuned for the simulation
"""
import datetime

# =============================================================================
# Variables to change
# =============================================================================
""" Car and charging related """
slowcharge_ulim = 3         # kW charging upper limit
fastcharge_ulim = 7         # kW charging upper limit
rapidcharge_ulim = 50       # kW charging upper limit

end_SOC_req = 0.8           # The achievable SOC at leaving below which car is given charging priority
priority_limit = 0.8        

carnumber = 100             # cars/day

buschargelength = 0.25      # hour of charging for 1 bus
busnumber = 17              # bus / day, 17 corresponds to bus/hour

vnumber = carnumber + busnumber     # Number of vehicles

""" Simulation related """
starttime = datetime.datetime(2020,3,30,6,0,0)     # Selected date for simulation, start time of simulation
endtime = datetime.datetime(2020,4,2,23,0)     # End time of simulation
time_increment = 0.05                 # [hours]


""" P&R operation related """
opentime = 6        # Opening time, hour
closetime = 23      # Closing time, hour
           

""" Finance related """
# Price of electricity, GPB per kWh
red_energy_cost = (14 + 5.363)/100         # Base rate + DUOS charge           
amber_energy_cost = (14 + 0.57)/100
green_energy_cost = (14 + 0.452)/100
