# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:55:45 2019

@author: Linh Pham Thi

This is a file to generate the random EV states
"""
import settings
from EVbattery import EVbattery
import random

# Initializing variables
evbatt = {}
total_ev_demand = 0         # Total number of kWh of the batteries that need to 
                            # be filled
total_inst_chargerate = 0   # The number of kW needed at the moment that - if
                            # sustained constantly, will change the cars fully
                            # by the time they leaves
                            
# Iterating to generate the EV battery attributes
for n in range(1,settings.carnumber+1):
        evbatt["EV{0}".format(n)]=EVbattery(32,random.uniform(0,1),random.gauss(7,2))
        total_ev_demand = total_ev_demand + evbatt["EV{0}".format(n)].fill
        total_inst_chargerate = total_inst_chargerate + evbatt["EV{0}".format(n)].avg_chargerate