# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules, initializing variables
# =============================================================================
import settings 
import showResults as sr

from simulation import simulation
from chargeRateBalance import chargeRateBalance
from datagen import datagen
from gridEnergyCalculator import gridEnergyCalculator

# =============================================================================
# Set up simulation and generate data
# =============================================================================
simulation = simulation(settings.starttime, settings.endtime, settings.time_increment)
    
# =============================================================================
# Simulation
# =============================================================================

while simulation.current_datetime < simulation.endtime:
    # =========================================================================
    # Generate a new set of data for EV batteries if it's a new day
    # =========================================================================
    if simulation.current_date != simulation.last_date:
        evbatt, total_ev_demand, total_inst_chargerate = datagen(simulation)
        
        for n in range (1, settings.vnumber + 1):
            evbatt["EV{0}".format(n)].statusUpdate(simulation)
        
            # For plotting
            sr.SOC_before_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
        
    # For plotting
    sr.x_axis.append(simulation.current_datetime)
    
    # =========================================================================
    # Calculating distribution and buy from grid
    # =========================================================================
    evbatt = chargeRateBalance(evbatt, simulation)
    evbatt = gridEnergyCalculator(evbatt, simulation)
    
    # =========================================================================
    # Charging
    # =========================================================================
    for n in range (1, settings.vnumber + 1):
        evbatt["EV{0}".format(n)].charge(simulation)
    
    # =========================================================================
    # Incrementing time
    # =========================================================================
    simulation.timeUpdate()
    
    for n in range (1, settings.vnumber + 1):    
        evbatt["EV{0}".format(n)].statusUpdate(simulation)

# =============================================================================
# Show results of the simulation
# =============================================================================
sr.showResults(evbatt, simulation)