# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:21:55 2019

author: Linh Pham Thi
"""

# =============================================================================
# Importing neccessary Python libraries and modules, initializing variables
# =============================================================================
import numpy as np
from ChargeRateBalance import ChargeRateBalance
import settings
import datagen

total_chargerate = 0

# =============================================================================
# Generate data and charge vehicles
# =============================================================================
evbatt, total_ev_demand, total_inst_chargerate = datagen.datagen()
evbatt, total_chargerate = ChargeRateBalance(evbatt)

# =============================================================================
# Calculating how much energy we need to buy from the grid at that moment
# =============================================================================
gridenergy = np.clip((total_chargerate - settings.pv_energy_profile[settings.hour]), 0, None)

print('Energy bought from the grid at that instant: ', gridenergy, ' kW')