# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules
# =============================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from EVbattery import EVbattery
from ChargeRateBalance import ChargeRateBalance
import settings
import datagen

# =============================================================================
# Checking current PV output and checking for excess
# =============================================================================
# pv_energy_profile = np.loadtxt('total_' + str(settings.month) + '_kWh.txt')
gridenergy = datagen.total_inst_chargerate - settings.pv_energy_profile[settings.hour]

#print('MOMENTARY DATA')
#print('Momentary demand: ', total_chargerate, 'kW')
#print('Momentary PV output: ', pv_energy_profile[hour], 'kW')
#print('Momentary energy we have to buy: ', gridenergy, 'kW')
#print('')

# Total energy balance based on expected daily PV output profile
total_pv_energy = np.trapz(pv_energy_profile[settings.hour:],x=settings.t,dx=settings.t_inc) #Using trapezoidal rule to integrate area under curve
total_gridenergy = datagen.total_ev_demand - total_pv_energy

print('DAILY DATA')
print('Total demand: ', total_ev_demand, 'kWh')
print('Total PV output: ', total_pv_energy, 'kWh')
print('Total energy we have to buy: ', total_gridenergy, 'kWh')
print('Total we have to pay for the electricity bought: ', total_gridenergy * settings.el_price, 'GBP')
        

ChargeRateBalance()