# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules, initializing variables
# =============================================================================
import settings
import datetime  
import showResults as sr

from ChargeRateBalance import ChargeRateBalance
from datagen import datagen
from gridEnergyCalculator import gridEnergyCalculator


# =============================================================================
# Generate data
# =============================================================================
evbatt, total_ev_demand, total_inst_chargerate = datagen()

for n in range(1,settings.carnumber+1):
    evbatt["EV{0}".format(n)].presentUpdate(settings.current_datetime)
    evbatt["EV{0}".format(n)].detNeedMaxCR()

    # For plotting
for n in range(1,settings.carnumber+1):
    sr.SOC_before_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
    
# =============================================================================
# Simulation
# =============================================================================
while settings.current_datetime < settings.endtime:
        # For plotting
    sr.x_axis.append(settings.current_datetime)
    
    # =========================================================================
    # Calculating distribution and buy from grid
    # =========================================================================
    evbatt, sr.pv_energy_available, sr.pv_leftover_energy = ChargeRateBalance(evbatt, sr.pv_leftover_energy)
    evbatt, sr.grid_energy_needed, sr.total_extra_energy_needed, sr.red_band_energy, sr.amber_band_energy, sr.green_band_energy \
        = gridEnergyCalculator(evbatt, sr.grid_energy_needed, sr.red_band_energy, sr.amber_band_energy, sr.green_band_energy)
        
        # For plotting
    sr.grid_energy.append(sr.total_extra_energy_needed)
    sr.unused_pv_energy.append(sr.pv_energy_available)
    
    # =========================================================================
    # Charging
    # =========================================================================
    for n in range(1,settings.carnumber+1):
        evbatt["EV{0}".format(n)].charge(evbatt["EV{0}".format(n)].chargerate,settings.t_inc,settings.current_datetime)
    
    # =========================================================================
    # Incrementing time
    # =========================================================================
    settings.current_datetime = settings.current_datetime + datetime.timedelta(hours=settings.t_inc)
    settings.current_date = datetime.date(settings.current_datetime.year, settings.current_datetime.month, settings.current_datetime.day)
    settings.current_time = datetime.time(settings.current_datetime.hour, settings.current_datetime.minute)
    settings.hour = settings.current_datetime.hour
    
    for n in range(1,settings.carnumber+1):    
        evbatt["EV{0}".format(n)].presentUpdate(settings.current_datetime)
    

# =============================================================================
# Show results of the simulation
# =============================================================================
sr.showResults(evbatt)