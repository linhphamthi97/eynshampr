# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

This file contains all the global variables and all variables that need to be
initialized or tuned for the simulation
"""
import numpy as np
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
current_datetime = datetime.datetime(2020,1,10,6,0,0)     # Selected date for simulation, start time of simulation
endtime = datetime.datetime(current_datetime.year,current_datetime.month,current_datetime.day,23,0)     # End time of simulation
t_inc = 0.05                 # Time increment for the simulation in hours
           

""" Finance related """
el_price = 0.13             # Price of electricity, in pounds per kWh


# =============================================================================
# Calculated variables
# =============================================================================
""" Simulation related """
# Start time of simulation, stored for visualization purposes
starttime = current_datetime    

# Copy times by value to avoid copy by reference
current_date = datetime.date(current_datetime.year, current_datetime.month, current_datetime.day)
current_time = datetime.time(current_datetime.hour, current_datetime.minute, 0)

month = current_datetime.month
hour = current_datetime.hour

""" Car and charging related """
pv_energy_profile = np.loadtxt('total_' + str(month) + '_kWh.txt')

""" Finance related """