# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:19:45 2019

@author: neilw
"""

def discountfactor(borrowing,inflation,year):
    """input borrowing rate and inflation rate to return discountfactor all in decimals""" 
    discountfactor = 1/(1+borrowing-inflation)**year
    return discountfactor

    