# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:19:09 2019

@author: Linh Pham Thi
"""
import datetime
import calendar

# =============================================================================
# Variables
# =============================================================================

class Simulation:
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
        self.leapyear = calendar.isleap(self.current_datetime.year)

        self.last_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day) - datetime.timedelta(days = 1)        
    
    def timeUpdate(self):
        self.last_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)

        self.current_datetime = self.current_datetime + datetime.timedelta(hours=self.t_inc)
        self.current_date = datetime.date(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)
        self.current_time = datetime.time(self.current_datetime.hour, self.current_datetime.minute)
        self.current_hour = self.current_datetime.hour      
        
    def rangepick(self):
    # Picks the range for the solar profile based on the date, taking into consideration leap years
        # Not a leap year
        if calendar.isleap(self.current_datetime.year) == 0:
            daycount = (self.current_datetime - datetime.datetime(self.current_date.year, 1, 1, 0, 0)).days

        # Leap year
        elif calendar.isleap(self.current_datetime.year) == 1:
            # Before February 29, indexing is the same as in non-leap years
            if self.current_date < datetime.date(self.current_date.year, 2, 29):
                daycount = (self.current_datetime - datetime.datetime(self.current_date.year, 1, 1, 0, 0)).days

            # February 29th is February 28th duplicated and after that, daycount is shifted by 1
            else:
                daycount = (self.current_datetime - datetime.timedelta (days = 1) - datetime.datetime(self.current_date.year, 1, 1, 0, 0)).days
                
        self.PVrange_begin = daycount * 24
        self.PVrange_end = (daycount + 1) * 24      # Not substracting one due to the indexing syntax of Python