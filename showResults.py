# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:59:43 2019

@author: Linh Pham Thi

This file is a function to show results, plot graphs
"""
import numpy as np
import settings

#Initialise variables
grid_energy_needed = 0
pv_leftover_energy = 0
red_band_energy = 0
amber_band_energy = 0
green_band_energy = 0
pv_energy_available = 0
grid_energy_needed_day = 0
unused_pv_energy_day = 0
total_sold_energy = 0
total_PV_energy = 0

SOC_before_plot = list()
SOC_after_plot = list()
x_axis = list()     # An x axis containing the timestamps of the simulation
longs_x_axis = list() # An x axis containing the days for long simulations
grid_energy = list()
unused_pv_energy = list()
daily_grid_energy = list()
daily_unused_pv_energy = list()

def showResults(evbatt, simulation):  
    
    # =========================================================================
    # Print energy balance values
    # =========================================================================


    # Cost of energy
    energy_cost = red_band_energy * settings.red_energy_cost \
                    + amber_band_energy * settings.amber_energy_cost \
                    + green_band_energy * settings.green_energy_cost
   
    
    return (np.around(total_sold_energy + grid_energy_needed, decimals = 1), int(energy_cost))
    
    


    


    


