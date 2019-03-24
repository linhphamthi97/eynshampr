# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 14:46:35 2019

@author: Linh Pham Thi
"""
import numpy as np
import datetime
import settings

class EVbattery:
    
    # =========================================================================
    # Initialising variables
    # =========================================================================
    def __init__(self, capacity, SOC, premium, chargetype, time, arrivaltime):

        # =====================================================================
        # Charging related
        # =====================================================================
        self.capacity = capacity  # kWh
        self.SOC = SOC  # proportion charged when arriving in P+R
        self.fill = self.capacity - self.capacity * self.SOC # kWh needed to completely fill battery
        self.chargetype = chargetype    # Type of charging (slow=0, fast=1)
        self.premium = premium          # Premium charging, i.e car is guaranteed to charge to 100% is physically possible
        
            # Charging rate limit
        if self.chargetype == 0:
            self.crlimit = settings.slowcharge_ulim
        else:
            self.crlimit = settings.fastcharge_ulim

        # =====================================================================
        # Time related
        # =====================================================================
        self.time = time # length of time car will be parked in hours (driver inputs on arrival)
        self.arrivaltime = arrivaltime # When the car arrives in the day
        self.leavetime = arrivaltime + datetime.timedelta(hours = self.time)
        self.present = 0    # If a car is present in the parking lot at a particular time
        
        # =====================================================================
        # For the algorithm's use
        # =====================================================================
        self.avg_chargerate = self.fill / self.time

        self.need_maxcharge = 0     # If this value is 1, that means that we cannot charge the car to at least 80% during it's stay
                                    # This means this car will always be charged at the maximum charging rate
        self.grid_perm = 0          # If this value is 1, then the car has 'permission' to buy energy from the grid to charge
                                    # If this value is 0, then the car cannot demand extra energy from the grid

        # Minimum charge duration for leaving SOC to hit the requirement (80%)
        if self.premium == 0:
            self.min_charge_dur = datetime.timedelta(hours = (settings.end_SOC_req - self.SOC)*self.capacity / self.crlimit)
        else:
            self.min_charge_dur = datetime.timedelta(hours = (1 - self.SOC) * self.capacity / self.crlimit)

        # Needs the maximum chargerate at all times when present?
        if self.time * self.crlimit <= (settings.end_SOC_req - self.SOC)*self.capacity:
            self.need_maxcharge = 1
        else: 
            self.need_maxcharge = 0
        
    # =========================================================================
    # This function charges the car by updating the relevant parameters
    # =========================================================================
    def charge(self, simulation):
        
        self.fill = np.clip((self.fill - self.chargerate * simulation.t_inc), 0, self.capacity)
#        self.SOC = (self.capacity - self.fill)/self.capacity   # This line is for debugging
        self.SOC = np.clip((self.capacity - self.fill) / self.capacity, 0, 1) # This is the real expression to use for final program
        self.avg_chargerate = np.clip(self.fill / ((self.leavetime - simulation.current_datetime).total_seconds()/3600) , 0 , None)


    # =========================================================================
    # This function updates the car's status
    # =========================================================================
    def statusUpdate(self, simulation):
        
        # Present at the site or not
        if (self.arrivaltime <= simulation.current_datetime) and (simulation.current_datetime <= self.leavetime):
            self.present = 1
        else:
            self.present = 0     

        # =====================================================================
        # Grid energy permission
        # =====================================================================     
        # If the car is not present then no grid energy demand
        if self.present == 0 :
            self.grid_perm = 0

        # If the car is present and need the maxinum chargerate, then allow grid energy demand
        elif self.need_maxcharge == 1:
            self.grid_perm = 1
            
        # If the car leaves before 7am then allow grid energy demand
        elif self.present == 1 and \
             datetime.time(self.leavetime.hour, self.leavetime.minute) <= datetime.time(7,0):
                 self.grid_perm = 1

        # If the car leaves between 7am and  4pm or it is the weekend, then only allow charging at (leavetime - min_charge_dur)
        elif datetime.time(self.leavetime.hour, self.leavetime.minute) <= datetime.time(16,0) or \
             simulation.current_date.weekday() > 4:
            if simulation.current_datetime >= (self.leavetime - self.min_charge_dur):
                self.grid_perm = 1
            else:
                self.grid_perm = 0


        # If the car leaves between 4pm and 7pm, then only allow charging at (4pm - min_chare_dur)
        elif datetime.time(self.leavetime.hour, self.leavetime.minute) <= datetime.time(19,0):
            if simulation.current_datetime >= datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 16,0) - self.min_charge_dur:

                # No charging in the red band time           
                if simulation.current_datetime > datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 16,0) and \
                    simulation.current_datetime < datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 19,0):
                        self.grid_perm = 0
                else: 
                    self.grid_perm = 1
            else:
                self.grid_perm = 0
                
        # If the car leaves after 7pm, then only allow charging at (leavetime - min_charge_dur - 3 hours) to avoid red band zone
        elif datetime.time(self.leavetime.hour, self.leavetime.minute) >= datetime.time(19,0):
            if simulation.current_datetime >= self.leavetime - self.min_charge_dur - datetime.timedelta (hours = 3):

                # No charging in the red band time           
                if simulation.current_datetime > datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 16,0) and \
                    simulation.current_datetime < datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 19,0):
                        self.grid_perm = 0
                else: 
                    self.grid_perm = 1
            else:
                self.grid_perm = 0

        else: 
            self.grid_perm = 0