# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 13:45:19 2019

@author: neilw
"""
import pandas as pd

def energydemand(proportionEVs):
    df2 = pd.read_csv('Timeseries_hourly_year.csv', usecols=[2]) #EVdemand
    df3 = pd.read_csv('Timeseries_hourly_year.csv', usecols=[3]) #electric bus demand
    energydemand = proportionEVs*10*df2.values + df3.values #kWh
    return energydemand
