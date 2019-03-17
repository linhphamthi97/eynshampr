# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 14:46:35 2019

@author: Linh Pham Thi
"""
import numpy as np
import datetime
import settings
import simulation

class EVbattery:
    
    # =========================================================================
    # Initialising variables
    # =========================================================================
    def __init__(self,capacity,SOC,time,chargetype,arrivaltime):
        # Charge related
        self.capacity = capacity  # kWh
        self.SOC = SOC  # proportion charged when arriving in P+R
        self.fill = self.capacity - self.capacity * self.SOC # kWh needed to completely fill battery
        self.chargetype = chargetype    # Type of charging (slow=0, fast=1) 
        
        # Time related
        self.time = time # length of time car will be parked in hours (driver inputs on arrival)
        self.arrivaltime = arrivaltime # When the car arrives in the day
        self.leavetime = arrivaltime + datetime.timedelta(hours = self.time)
        self.present = 0    # If a car is present in the parking lot at a particular time
        
        # Calculated, for the algorithm's use
        self.avg_chargerate = self.fill / self.time # actual kWh given length of stay

        self.need_maxcharge = 0     # If this value is 1, that means that we cannot charge the car to at least 80% during it's stay
                                    # This means this car will always be charged at the maximum charging rate
        
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
        
        # Latest time the car can start charging at maximum rate if we want to fill it up completely                            
        if self.chargetype == 0:
            self.latest_maxCR_start = self.arrivaltime + datetime.timedelta(hours = self.time) - datetime.timedelta(hours = self.fill / settings.slowcharge_ulim)
        else:
            self.latest_maxCR_start = self.arrivaltime + datetime.timedelta(hours = self.time) - datetime.timedelta(hours = self.fill / settings.fastcharge_ulim)

        
    # =========================================================================
    # This function needs to be ran only at the beginning of the simulation 
    # =========================================================================
    def detNeedMaxCR(self):
        if self.chargetype == 0:
            if self.time * settings.slowcharge_ulim <= (settings.end_SOC_req - self.SOC)*self.capacity:
                self.need_maxcharge = 1
                
        else: 
            if self.time * settings.fastcharge_ulim <= (settings.end_SOC_req - self.SOC)*self.capacity:
                self.need_maxcharge = 1