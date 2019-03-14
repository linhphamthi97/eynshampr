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
import matplotlib.dates as mdates

from ChargeRateBalance import ChargeRateBalance
from datagen import datagen
from gridEnergyCalculator import gridEnergyCalculator

grid_energy_needed = 0
pv_leftover_energy = 0
red_band_energy = 0
amber_band_energy = 0
green_band_energy = 0
grid_energy=list()
x_axis = list()

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
    
    # For plotting
    x_axis.append(settings.current_datetime)
    
    # =========================================================================
    # Calculating distribution and buy from grid
    # =========================================================================
    evbatt, pv_energy_available, pv_leftover_energy = ChargeRateBalance(evbatt, pv_leftover_energy)
    evbatt, grid_energy_needed, total_extra_energy_needed, red_band_energy, amber_band_energy, green_band_energy \
        = gridEnergyCalculator(evbatt, grid_energy_needed, red_band_energy, amber_band_energy, green_band_energy)
        
    # For plotting
    grid_energy.append(total_extra_energy_needed)
    
    # =========================================================================
    # Charging
    # =========================================================================
    for n in range(1,settings.carnumber+1):
        total_chargerate += evbatt["EV{0}".format(n)].chargerate
        
        evbatt["EV{0}".format(n)].charge(evbatt["EV{0}".format(n)].chargerate,settings.t_inc,settings.current_datetime)
    
    # Incrementing time
    settings.current_datetime = settings.current_datetime + datetime.timedelta(hours=settings.t_inc)
    settings.current_date = datetime.date(settings.current_datetime.year, settings.current_datetime.month, settings.current_datetime.day)
    settings.current_time = datetime.time(settings.current_datetime.hour, settings.current_datetime.minute)
    settings.hour = settings.current_datetime.hour
    
    for n in range(1,settings.carnumber+1):    
        evbatt["EV{0}".format(n)].presentUpdate(settings.current_datetime)
    
# =============================================================================
# Plotting and showing results
# =============================================================================
""" Energy balances """
print('Leftover energy: ', np.clip(pv_leftover_energy, 0, None), ' kWh')
print('')
print('Total energy bought from the grid: ', grid_energy_needed, ' kWh')
print('Red band energy bought from the grid: ', red_band_energy, ' kWh')
print('Amber band energy bought from the grid: ', amber_band_energy, ' kWh')
print('Green band energy bought from the grid: ', green_band_energy, ' kWh')
print('')
print('Cost of energy bought from the grid: ', grid_energy_needed * settings.el_price, ' GBP')


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

# Plotting a graph of the grid energy bought
plt.plot(x_axis,grid_energy,'black')
plt.gcf().autofmt_xdate()
myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)
plt.ylim(bottom=0)
plt.title('Energy bought from the grid')
plt.xlabel('Time')
plt.ylabel('Energy [kWh]')

    # Creating the time bands based on DUOS charges
plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, settings.starttime.hour, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,7,0), facecolor='green', alpha=0.5)
plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 7, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,16,0), facecolor='yellow', alpha=0.5)
plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 16, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,19,0), facecolor='red', alpha=0.5)
plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 19, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,23,0), facecolor='yellow', alpha=0.5)
plt.axvspan(datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day, 23, 0), datetime.datetime(settings.starttime.year,settings.starttime.month,settings.starttime.day,23,59), facecolor='green', alpha=0.5)

plt.show()