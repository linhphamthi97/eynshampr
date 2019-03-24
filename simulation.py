# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:19:09 2019

@author: Linh Pham Thi
"""
import datetime
import settings

# =============================================================================
# Variables
# =============================================================================

class simulation:
    def __init__(self,starttime, endtime, t_inc):
        self.starttime = starttime
        self.endtime = endtime
        self.t_inc = t_inc
        
        self.current_datetime = starttime
        self.current_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)
        self.current_time = datetime.time(self.current_datetime.hour, self.current_datetime.minute)
        self.current_hour = self.current_datetime.hour        
    
    def timeUpdate(self):
        self.current_datetime = self.current_datetime + datetime.timedelta(hours=self.t_inc)
        self.current_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)
        self.current_time = datetime.time(self.current_datetime.hour, self.current_datetime.minute)
        self.current_hour = self.current_datetime.hour
        
    
