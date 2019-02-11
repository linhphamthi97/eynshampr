# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

This file contains all the global variables and all variables that need to be
initialized
"""
import numpy as np

# =============================================================================
# Initializing variables
# =============================================================================
# Variables to change
carnumber = 100
month = 1
hour = 9                    # This will be incremented later to simulate passing time
el_price = 0.13             # Price of electricity, in pounds per kWh
t_inc=0.05                   # Time increment for the simulation
t = range(hour,25)          # Hours in a day
slowcharge_ulim = 7         # kW charging
fastcharge_ulim = 22         # kW charging

#Variables calculated
pv_energy_profile = np.loadtxt('total_' + str(month) + '_kWh.txt')

