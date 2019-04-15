# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules, initializing variables
# =============================================================================
import warnings
warnings.filterwarnings("ignore")


import settings 
import datetime

import showResults as sr

from simulation import simulation
from settings import chargeRateBalance
from datagen import datagen
from gridEnergyCalculator import gridEnergyCalculator
#==============================================================================
#change variables in settings
#==============================================================================


# =============================================================================
# Set up simulation and PV
# =============================================================================
simulation = simulation(settings.starttime, settings.endtime, settings.time_increment)
solar_profile = settings.pv_site1.getOutput(settings.dt)
    
# =============================================================================
# Simulation
# =============================================================================

while simulation.current_datetime < simulation.endtime:
    # =========================================================================
    # Generate a new set of data for every new day, add totals of last day to results
    # =========================================================================
    if simulation.current_date != simulation.last_date:
        evbatt, total_ev_demand, total_inst_chargerate = datagen(simulation)
        
        for n in range (1, settings.vnumber + 1):
            evbatt["EV{0}".format(n)].statusUpdate(simulation)
        

        # Picks the range for solar profile corresponding to the day
        simulation.rangepick()
        

    # =========================================================================
    # Calculating distribution and buy from grid
    # =========================================================================
    evbatt = chargeRateBalance(evbatt, simulation, solar_profile)
    for n in range (1, settings.vnumber + 1):
        sr.total_sold_energy += evbatt["EV{0}".format(n)].chargerate * simulation.t_inc   
    
#    for n in range (1, settings.vnumber + 1):
#            evbatt["EV{0}".format(n)].grid_perm = 1
    
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
# Show results of the simulation in tuple 0.total electricity sold 1.cost of buying from grid
# =============================================================================


print(sr.showResults(evbatt, simulation)[0])
print(sr.showResults(evbatt, simulation)[1])
