# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:58:09 2019

@author: Nicole
"""

import matplotlib.pyplot as plt
import pandas as pd
from energydemand import energydemand

def energydeficit(numberPVs,efficiencyPV,proportionEVs):
 
    areaPV = 1.59004 * 1.0541 # m^2
    areacovered = areaPV*numberPVs #m^2 (area of parking spaces covered, 12000m^2 maximum)
    df1 = pd.read_csv('Timeseries_hourly_year.csv', usecols=[1])
    energygeneration = efficiencyPV*areacovered*df1.values/1000 #kWh
    
    #max number of PVs is 7000, given that there are 21 panels per 3 bays, with 1000 bays in total
    
    energy_demand = energydemand(proportionEVs)
    
    #proportion of EVs relative to total car park users assumed to be 10% for first phase
    
    energydeficit = energygeneration - energy_demand #kWh
    
    plt.plot(energydeficit)
    plt.title('Energy generation - energy demand')
    plt.ylabel('Energy deficit (kWh)')
    plt.xlabel('Time in a year (hours)')
    energy_import=[]
    for i in range(len(energydeficit)):
        if energydeficit[i]<0:
            energy_import.append(energydeficit[i])
        else:
            energy_import.append(0)
            
    return energy_import
    
