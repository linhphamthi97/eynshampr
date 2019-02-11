# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 14:46:35 2019

@author: QUDILIVI
"""

class EVbattery:
    
    def __init__(self,capacity,SOC,time,ctype):
        self.capacity = capacity # kWh
        self.SOC = SOC # proportion charged when arriving in P+R
        self.time = time # length of time car will be parked in hours (driver inputs on arrival)
        self.fill = self.capacity - self.capacity * self.SOC # kWh needed to completely fill battery
        self.avg_chargerate = self.fill / self.time # actual kWh given length of stay
        self.chargetype = ctype    # Type of charging (slow=0, fast=1) 

    def charge(self,chargerate,t_inc):
        
        self.fill = self.fill - chargerate*t_inc
        self.SOC = (self.capacity - self.fill)/self.capacity