# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 14:46:35 2019

@author: Linh Pham Thi
"""
import numpy as np
import datetime

class EVbattery:
    
    def __init__(self,capacity,SOC,time,ctype,arrivaltime):
        self.capacity = capacity  # kWh
        self.SOC = SOC  # proportion charged when arriving in P+R
        self.time = time # length of time car will be parked in hours (driver inputs on arrival)
        self.fill = self.capacity - self.capacity * self.SOC # kWh needed to completely fill battery
        self.avg_chargerate = self.fill / self.time # actual kWh given length of stay
        self.chargetype = ctype    # Type of charging (slow=0, fast=1) 
        self.arrivaltime = arrivaltime # When the car arrives in the day
        self.present = 0    # If a car is present in the parking lot at a particular time

    def charge(self,chargerate,t_inc,current_time):
        self.fill = self.fill - self.chargerate*t_inc
#        self.SOC = (self.capacity - self.fill)/self.capacity   # This line is for debugging
        self.SOC = np.clip((self.capacity - self.fill)/self.capacity,0,1) # This is the real expression to use for final program
        self.avg_chargerate = np.clip(self.fill / ((self.arrivaltime + datetime.timedelta(hours = self.time) - current_time).total_seconds()/3600) , 0 , None)
        
    def presentUpdate(self,current_datetime):
        if self.arrivaltime <= current_datetime and current_datetime <= (self.arrivaltime + datetime.timedelta(hours = self.time)):
            self.present = 1
        else:
            self.present = 0