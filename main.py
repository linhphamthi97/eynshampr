# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules, initializing variables
# =============================================================================
import numpy as np
import settings
import matplotlib.pyplot as plt
import datetime  

from ChargeRateBalance import ChargeRateBalance
from datagen import datagen
from gridEnergyCalculator import gridEnergyCalculator

grid_energy_needed = 0
pv_leftover_energy = 0

# =============================================================================
# Generate data
# =============================================================================
evbatt, total_ev_demand, total_inst_chargerate = datagen()
for n in range(1,settings.carnumber+1):
    evbatt["EV{0}".format(n)].presentUpdate(settings.current_datetime)

# For showing results
SOC_before_plot=list()
for n in range(1,settings.carnumber+1):
#    print('SOC for EV',n,' before charging: ',evbatt["EV{0}".format(n)].SOC*100,'%')
    SOC_before_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
    
# =============================================================================
# Simulation
# =============================================================================
while settings.current_datetime < settings.endtime:
    # Initialise variables
    total_chargerate = 0
    
    # =========================================================================
    # Calculating distribution and buy from grid
    # =========================================================================
    evbatt, pv_energy_available, pv_leftover_energy = ChargeRateBalance(evbatt, pv_leftover_energy)
    evbatt, grid_energy_needed = gridEnergyCalculator(evbatt, grid_energy_needed)
    
    # =========================================================================
    # Charging
    # =========================================================================
    for n in range(1,settings.carnumber+1):
        total_chargerate += evbatt["EV{0}".format(n)].chargerate
        
        evbatt["EV{0}".format(n)].charge(evbatt["EV{0}".format(n)].chargerate,settings.t_inc,settings.current_datetime)
    
    # Incrementing time
    settings.current_datetime = settings.current_datetime + datetime.timedelta(hours=settings.t_inc)
    
    for n in range(1,settings.carnumber+1):    
        evbatt["EV{0}".format(n)].presentUpdate(settings.current_datetime)
    
# =============================================================================
# Plotting and showing results
# =============================================================================
""" Energy balances """
print('Leftover energy: ', np.clip(pv_leftover_energy, 0, None), ' kWh')
print('Total energy bought from the grid: ', grid_energy_needed * settings.t_inc, ' kWh')
print('Cost of energy bought from the grid: ', grid_energy_needed * settings.t_inc * settings.el_price, ' GBP')


""" SOC graphs"""
SOC_after_plot=list()

for n in range(1,settings.carnumber+1):
#    print('SOC for EV',n,' after charging: ',evbatt["EV{0}".format(n)].SOC*100,'%')
    
    # For plotting
    SOC_after_plot.append(evbatt["EV{0}".format(n)].SOC * 100)

# Plotting a graph of the SOC
#Before
y_axis = np.linspace(1,settings.carnumber,settings.carnumber) 
plt.rcParams["figure.figsize"] = [8,6]
plt.barh(y_axis, SOC_before_plot)
plt.ylim(bottom=0)
plt.title('State of charge of the EVs before charging')
plt.xlabel('State of charge [%]')
plt.show()

#After
y_axis = np.linspace(1,settings.carnumber,settings.carnumber) 
plt.rcParams["figure.figsize"] = [8,6]
plt.barh(y_axis, SOC_after_plot)
plt.ylim(bottom=0)
plt.title('State of charge of the EVs after charging')
plt.xlabel('State of charge [%]')
plt.show()