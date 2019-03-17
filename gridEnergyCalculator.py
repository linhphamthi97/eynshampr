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
import showResults as sr


def gridEnergyCalculator(evbatt, simulation):
    total_extra_energy_needed = 0
    
    for n in range (1, settings.carnumber + 1):
        
        #======================================================================
        # Picking out the EVs that after the energy division are charging at a 
        # sub-optimal rate (less than the average charging rate) and buying in
        # energy from the grid to match that average charging rate.
        #
        # Conditions to buy from the grid:
        #   - charging rate less than it's charging limit
        #   - SOC less than 0.8, i.e our goal for the leaving SOC
        #   - the EV is present at the site
        #   - permission to buy from the grid
        #======================================================================      
        extra_energy_needed = 0
        
        # Slow charge
        if evbatt["EV{0}".format(n)].chargetype == 0 and \
           (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim)) and \
           (evbatt["EV{0}".format(n)].SOC < settings.end_SOC_req) and \
           evbatt["EV{0}".format(n)].present == 1 and \
           evbatt["EV{0}".format(n)].grid_perm == 1:

               if evbatt["EV{0}".format(n)].need_maxcharge == 1:
                   extra_energy_needed = settings.slowcharge_ulim - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = settings.slowcharge_ulim                   
               else:
                   extra_energy_needed = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim) - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.slowcharge_ulim)
        # Fast charge
        elif evbatt["EV{0}".format(n)].chargetype == 1 and \
             (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,settings.fastcharge_ulim)) and \
             (evbatt["EV{0}".format(n)].SOC < settings.end_SOC_req) and \
             evbatt["EV{0}".format(n)].present == 1 and \
             evbatt["EV{0}".format(n)].grid_perm == 1:

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
        sr.grid_energy_needed += extra_energy_needed * simulation.t_inc    # Goes towards total energy bought during the day
        total_extra_energy_needed += extra_energy_needed * simulation.t_inc   # Goes towards total energy bought during that time instant, mainly for visualising
        
        # Weekday
        if simulation.current_date.weekday() < 5:
            if simulation.current_time >= datetime.time(16,0) and simulation.current_time < datetime.time(19,0):
                sr.red_band_energy += extra_energy_needed * simulation.t_inc
            elif (simulation.current_time >= datetime.time(7,0) and simulation.current_time < datetime.time(16,0)) \
                 or\
                 (simulation.current_time >= datetime.time(19,0) and simulation.current_time < datetime.time(23,0)):
                     sr.amber_band_energy += extra_energy_needed * simulation.t_inc
            elif (simulation.current_time >= datetime.time(0,0) and simulation.current_time < datetime.time(7,0)) \
                 or\
                 simulation.current_time >= datetime.time(23,0):
                     sr.green_band_energy += extra_energy_needed * simulation.t_inc
        
        # Weekend
        else: 
            sr.green_band_energy += extra_energy_needed * simulation.t_inc
    
    #==========================================================================
    # For plotting
    #==========================================================================
    sr.grid_energy.append(total_extra_energy_needed)
                     
    return evbatt