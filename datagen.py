# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:55:45 2019

@author: Linh Pham Thi

This is a file to generate the random instances for the EVbattery class
"""
import settings
from EVbattery import EVbattery
import random
import datetime
import numpy as np
import simulation

def datagen(simulation):
    # Initializing variables
    evbatt = {}
    total_ev_demand = 0         # Total number of kWh of the batteries that need to 
                                # be filled
    total_inst_chargerate = 0   # The number of kW needed at the moment that - if
                                # sustained constantly, will change the cars fully
                                # by the time they leaves
                                
    # Iterating to generate the EV battery attributes
    for n in range(1,(settings.carnumber+1)):
                                                # Battery capacity        
            evbatt["EV{0}".format(n)]=EVbattery(32,\
                                                # State of charge
                                                np.clip(random.gauss(0.5,0.15), 0, None),\
                                                # Length of stay in hours
                                                random.gauss(7,2),\
                                                # Type of charging, 0 for slow, 1 for fast
                                                random.randint(0,1),\
                                                # Time of arrival, year, month, day set in settings, hour and minute randomized
                                                datetime.datetime(simulation.current_datetime.year,simulation.current_datetime.month,\
#                                                                  settings.current_datetime.day,random.randint(6,20),random.randint(0,59)))
                                                                  simulation.current_datetime.day,int(np.clip(random.gauss(8,3),6,23)), random.randint(0,59)))
            total_ev_demand = total_ev_demand + evbatt["EV{0}".format(n)].fill
            total_inst_chargerate = total_inst_chargerate + evbatt["EV{0}".format(n)].avg_chargerate
            
    return evbatt, total_ev_demand, total_inst_chargerate