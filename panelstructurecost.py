# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 00:29:52 2019

@author: neilw
"""
import math
"""data of upfront costs per bay"""
def initial(num_bays):
    #Cost for Foundation and structure per bay
    materials=579.29
    fixed_delivery=(math.ceil(num_bays/48)-1)*1614
    costlabour=49.51+16.26
    temporarysite=costlabour*0.1
    installation=83.84
    lighting=418.80/3
    chargepoint=1800
    #cost for solar power system per additional bay
    additionalsystem=1555.09
    #cost for solar power system for whole plant
    wholeplant=804.42
    
    initial= (materials+installation+temporarysite+additionalsystem+lighting+chargepoint)*num_bays+wholeplant+fixed_delivery
    return initial


