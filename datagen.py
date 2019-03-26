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

def datagen(simulation):
    # Initializing variables
    evbatt = {}
    total_ev_demand = 0         # Total number of kWh of the batteries that need to 
                                # be filled
    total_inst_chargerate = 0   # The number of kW needed at the moment that - if
                                # sustained constantly, will change the cars fully
                                # by the time they leaves                       
    
    # Creating instances of the EV battery class
    for n in range(1,(settings.carnumber + settings.busnumber + 1)):
        # CAR instances
        if n <= settings.carnumber:
                                                # Battery capacity        
            evbatt["EV{0}".format(n)]=EVbattery(32,\
                                                # State of charge
                                                np.clip(random.gauss(0.5,0.15), 0, None),\
                                                # Premium charging?
                                                random.choices([0, 1], weights = [9, 1], k = 1), \
                                                # Type of charging, 0 for slow, 1 for fast
                                                random.randint(0,1),\
                                                # Length of stay in hours
                                                random.gauss(7,2),\
                                                # Time of arrival, year, month, day set in settings, hour and minute randomized
                                                datetime.datetime(simulation.current_datetime.year,simulation.current_datetime.month,\
                                                                  simulation.current_datetime.day,int(np.clip(random.gauss(8,3),6,23)), random.randint(0,59)))
        # BUS instances
        else: 
                                                # Battery capacity        
            evbatt["EV{0}".format(n)]=EVbattery(320,\
                                                # State of charge
                                                np.clip(random.gauss(0.5,0.15), 0, None),\
                                                # Premium charging?
                                                0, \
                                                # Type of charging, 0 for slow, 1 for fast
                                                2,\
                                                # Length of stay in hours
                                                settings.buschargelength,\
                                                # Time of arrival, year, month, day set in settings, hour and minute randomized
                                                datetime.datetime(simulation.current_datetime.year,simulation.current_datetime.month,\
                                                                  simulation.current_datetime.day,5,0) + \
                                                                  datetime.timedelta (hours = (settings.closetime - settings.opentime) / settings.busnumber) * (n - settings.carnumber))

            total_ev_demand = total_ev_demand + evbatt["EV{0}".format(n)].fill
            total_inst_chargerate = total_inst_chargerate + evbatt["EV{0}".format(n)].avg_chargerate
            
    
    return evbatt, total_ev_demand, total_inst_chargerate