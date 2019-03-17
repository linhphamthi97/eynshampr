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
carnumber = 100
slowcharge_ulim = 3         # kW charging upper limit
fastcharge_ulim = 7         # kW charging upper limit

end_SOC_req = 0.8           # The achievable SOC at leaving below which car is given charging priority


""" Simulation related """
starttime = datetime.datetime(2020,12,10,6,0,0)     # Selected date for simulation, start time of simulation
endtime = datetime.datetime(starttime.year,starttime.month,starttime.day,23,0)     # End time of simulation
time_increment = 0.05                 # [hours]
           

""" Finance related """
# Price of electricity, GPB per kWh
red_energy_cost = (14 + 5.363)/100         # Base rate + DUOS charge           
amber_energy_cost = (14 + 0.57)/100
green_energy_cost = (14 + 0.452)/100
