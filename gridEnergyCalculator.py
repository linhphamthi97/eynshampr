# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:02:56 2019

@author: Linh Pham Thi

This function calculates the energy we have to buy from the grid based on the 
predicted PV output for the rest of the day.
"""
import settings
import numpy as np
import datetime


def gridEnergyCalculator(evbatt, total_grid_energy_needed, red_band_energy, amber_band_energy, green_band_energy):
    total_extra_energy_needed = 0
    
    for n in range(1,settings.carnumber+1):
        
        #======================================================================
        # Picking out the EVs that after the energy division are charging at a 
        # sub-optimal rate (less than the average charging rate) and buying in
        # energy from the grid to match that average charging rate
        #======================================================================      
        extra_energy_needed = 0
        
        # Slow charge
        if evbatt["EV{0}".format(n)].chargetype == 0 and \
           (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim)) and \
           (evbatt["EV{0}".format(n)].SOC < 1) and \
           evbatt["EV{0}".format(n)].present == 1:

               if evbatt["EV{0}".format(n)].need_maxcharge == 1:
                   extra_energy_needed = settings.slowcharge_ulim - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = settings.slowcharge_ulim                   
               else:
                   extra_energy_needed = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim) - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim)
        # Fast charge
        elif evbatt["EV{0}".format(n)].chargetype == 1 and \
             (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim)) and \
             (evbatt["EV{0}".format(n)].SOC < 1) and \
             evbatt["EV{0}".format(n)].present == 1:

               if evbatt["EV{0}".format(n)].need_maxcharge == 1:
                   extra_energy_needed = settings.fastcharge_ulim - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = settings.fastcharge_ulim                   
               else:
                   extra_energy_needed = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim) - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim)
                 
        #======================================================================
        # Categorizing the energy used into the time bands for finance applications
        #======================================================================
        # Summing up total energy bought from the grid
        total_grid_energy_needed += extra_energy_needed * settings.t_inc    # Goes towards total energy bought during the day
        total_extra_energy_needed += extra_energy_needed * settings.t_inc   # Goes towards total energy bought during that time instant, mainly for visualising
        
        # Weekday
        if settings.current_date.weekday() < 5:
            if settings.current_time >= datetime.time(16,0) and settings.current_time < datetime.time(19,0):
                red_band_energy += extra_energy_needed * settings.t_inc
            elif (settings.current_time >= datetime.time(7,0) and settings.current_time < datetime.time(16,0)) \
                 or\
                 (settings.current_time >= datetime.time(19,0) and settings.current_time < datetime.time(23,0)):
                     amber_band_energy += extra_energy_needed * settings.t_inc
            elif (settings.current_time >= datetime.time(0,0) and settings.current_time < datetime.time(7,0)) \
                 or\
                 settings.current_time >= datetime.time(23,0):
                     green_band_energy += extra_energy_needed * settings.t_inc
        
        # Weekend
        else: 
            green_band_energy += extra_energy_needed * settings.t_inc
    
                
    return evbatt, total_grid_energy_needed, total_extra_energy_needed, red_band_energy, amber_band_energy, green_band_energy