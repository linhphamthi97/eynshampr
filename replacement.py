# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 01:28:03 2019

@author: neilw
"""
import math
def replace(num_bays):
    fixed_delivery=(math.ceil(num_bays/48)-1)*1614
    #replacement every ten years
    return (901.50+819.57+1166.32)*num_bays+750+603.32+fixed_delivery
    
    
    