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
        
            # For plotting
            sr.SOC_before_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
        
        # Picks the range for solar profile corresponding to the day
        simulation.rangepick()
        
        # For plotting
        sr.longs_x_axis.append(simulation.current_date)
        sr.daily_grid_energy.append(sr.grid_energy_needed_day)
        sr.grid_energy_needed_day = 0
        sr.daily_unused_pv_energy.append(sr.unused_pv_energy_day)
        sr.unused_pv_energy_day = 0
        
    # For plotting
    sr.x_axis.append(simulation.current_datetime)
    
    # =========================================================================
    # Calculating distribution and buy from grid
    # =========================================================================
    evbatt = chargeRateBalance(evbatt, simulation, solar_profile)
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
sr.longs_x_axis.append(simulation.current_date)
sr.daily_grid_energy.append(sr.grid_energy_needed_day)
sr.daily_unused_pv_energy.append(sr.unused_pv_energy_day)

sr.showResults(evbatt, simulation)