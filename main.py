# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules
# =============================================================================
import numpy as np
from ChargeRateBalance import ChargeRateBalance
import settings
import datagen

evbatt, total_ev_demand, total_inst_chargerate = datagen.datagen()

# =============================================================================
# Checking current PV output and checking for excess
# =============================================================================
# pv_energy_profile = np.loadtxt('total_' + str(settings.month) + '_kWh.txt')
gridenergy = total_inst_chargerate - settings.pv_energy_profile[settings.hour]

# Total energy balance based on expected daily PV output profile
# Using trapezoidal rule to integrate area under curve
total_pv_energy = np.trapz(settings.pv_energy_profile[settings.hour:],x=settings.t,dx=settings.t_inc) 
total_gridenergy = total_ev_demand - total_pv_energy

print('DAILY DATA')
print('Total demand: ', total_ev_demand, 'kWh')
print('Total PV output: ', total_pv_energy, 'kWh')
print('Total energy we have to buy: ', total_gridenergy, 'kWh')
print('Total we have to pay for the electricity bought: ', total_gridenergy * settings.el_price, 'GBP')
print('')
        
evbatt, total_chargerate = ChargeRateBalance(evbatt)