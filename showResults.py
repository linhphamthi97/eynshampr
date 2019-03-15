# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:59:43 2019

@author: Linh Pham Thi

This file is a function to show results, plot graphs
"""
import numpy as np
import settings
import matplotlib.pyplot as plt
import datetime  
import matplotlib.dates as mdates

#Initialise variables
grid_energy_needed = 0
pv_leftover_energy = 0
red_band_energy = 0
amber_band_energy = 0
green_band_energy = 0
pv_energy_available = 0

SOC_before_plot = list()
SOC_after_plot = list()
x_axis = list()     # An x axis containing the timestamps of the simulation
grid_energy = list()
unused_pv_energy = list()

def showResults(evbatt):
    
    # =========================================================================
    # Print energy balance values
    # =========================================================================
    total_daily_pv_energy = 0
    for n in range (1,25):
        total_daily_pv_energy += settings.pv_energy_profile[n]
    print('Total daily PV energy: ' , total_daily_pv_energy)

    print('Leftover energy: ', np.clip(pv_leftover_energy, 0, None), ' kWh')
    print('')
    print('Total energy bought from the grid: ', grid_energy_needed, ' kWh')
    print('Red band energy bought from the grid: ', red_band_energy, ' kWh')
    print('Amber band energy bought from the grid: ', amber_band_energy, ' kWh')
    print('Green band energy bought from the grid: ', green_band_energy, ' kWh')
    print('')
    print('Cost of energy bought from the grid: ', grid_energy_needed * settings.el_price, ' GBP')
    
    
    # =========================================================================
    # SOC graphs
    # =========================================================================
    for n in range(1,settings.carnumber+1):
        SOC_after_plot.append(evbatt["EV{0}".format(n)].SOC * 100)
    
    """ Before """
    y_axis = np.linspace(1,settings.carnumber,settings.carnumber) 
    plt.rcParams["figure.figsize"] = [8,6]
    plt.barh(y_axis, SOC_before_plot)
    plt.ylim(bottom=0)
    plt.title('State of charge of the EVs before charging')
    plt.xlabel('State of charge [%]')
    plt.show()
    
    """ After """
    y_axis = np.linspace(1,settings.carnumber,settings.carnumber) 
    plt.rcParams["figure.figsize"] = [8,6]
    plt.barh(y_axis, SOC_after_plot)
    plt.ylim(bottom=0)
    plt.title('State of charge of the EVs after charging')
    plt.xlabel('State of charge [%]')
    plt.show()
    
    # =========================================================================
    # Grid energy demand graph (how much energy is bought from the grid vs time)
    # =========================================================================
    plt.plot(x_axis,grid_energy,'black')
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.ylim(bottom = 0)
    plt.xlim(left = settings.starttime , right = settings.endtime)
    plt.title('Energy bought from the grid')
    plt.xlabel('Time')
    plt.ylabel('Energy [kWh]')
    
    """ Creating the time bands based on DUOS charges """
    plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, settings.starttime.hour, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,7,0), facecolor='green', alpha=0.5)
    plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 7, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,16,0), facecolor='yellow', alpha=0.5)
    plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 16, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,19,0), facecolor='red', alpha=0.5)
    plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 19, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,23,0), facecolor='yellow', alpha=0.5)
    plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 23, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,23,59), facecolor='green', alpha=0.5)
    
    plt.show()
    
    # =========================================================================
    # Unused PV energy graph (how much PV energy is left unused vs time)
    # =========================================================================
    plt.plot(x_axis,unused_pv_energy,'black')
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.ylim(bottom = 0)
    plt.xlim(left = settings.starttime , right = settings.endtime)
    plt.title('Unused PV energy throughout the day')
    plt.xlabel('Time')
    plt.ylabel('Energy [kWh]')
    plt.show()    