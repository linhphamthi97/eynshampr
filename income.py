# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 00:35:00 2019

@author: neilw
"""

"""income"""
def income(num_spaces,threeWCost,sevenWCost,fiftyWCost,threeW,sevenW,fiftyW):
    """ advertising revenue per parking space 18 avg per space"""
    
    advertising = 18 * num_spaces
    
    income = advertising+threeWCost*threeW+sevenWCost*sevenW+fiftyWCost*fiftyW
    return income

