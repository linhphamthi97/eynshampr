# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

This file contains all the global variables and all variables that need to be
initialized
"""
import numpy as np
import datetime 


# =============================================================================
# Initializing variables
# =============================================================================
# Variables to change
carnumber = 100
current_datetime = datetime.datetime(2020,1,10,7,0)     # Selected date for simulation, start time of simulation
current_date = current_datetime.date
current_time = current_datetime.time
endtime = datetime.datetime(current_datetime.year,current_datetime.month,current_datetime.day,22,0)     # End time of simulation
month = current_datetime.month
hour = current_datetime.hour
t_inc = 0.05                 # Time increment for the simulation in hours
           
el_price = 0.13             # Price of electricity, in pounds per kWh

slowcharge_ulim = 3         # kW charging
fastcharge_ulim = 7         # kW charging

#Variables calculated
pv_energy_profile = np.loadtxt('total_' + str(month) + '_kWh.txt')

