# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:19:09 2019

@author: Linh Pham Thi
"""
import datetime

# =============================================================================
# Variables
# =============================================================================

class simulation:
    def __init__(self,starttime, endtime, t_inc):
        self.starttime = starttime
        self.starttime_date = datetime.date(self.starttime.year, self.starttime.month, self.starttime.day)
        self.endtime = endtime
        self.endtime_date = datetime.date(self.endtime.year, self.endtime.month, self.endtime.day)
        
        self.t_inc = t_inc
        
        self.current_datetime = starttime
        self.current_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)
        self.current_time = datetime.time(self.current_datetime.hour, self.current_datetime.minute)
        self.current_hour = self.current_datetime.hour

        self.last_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day) - datetime.timedelta(days = 1)        
    
    def timeUpdate(self):
        self.last_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)

        self.current_datetime = self.current_datetime + datetime.timedelta(hours=self.t_inc)
        self.current_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)
        self.current_time = datetime.time(self.current_datetime.hour, self.current_datetime.minute)
        self.current_hour = self.current_datetime.hour      
    
