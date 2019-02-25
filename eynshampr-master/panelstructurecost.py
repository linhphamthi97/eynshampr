# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 00:29:52 2019

@author: neilw
"""

"""data of upfront costs per bay"""
def structurecost(num_bays):
    invertor=2000
    fuelins_estimate = 30 
   
    """structure"""

    """screw piles £285 each (5% discount applied for orders over 50), 4 required per 3 space bay"""
    foundationmaterials = 4 * 285 * num_bays
    """screw pile installation 
    £600+£588 (equipment and excavator)per week with £300 deposit, £60 delivery
    fuel costs
    insurance"""

    """ weekly hire/hours in week 1hour per bay"""
    equipment = (600+588)/40*num_bays + 300 + 60 +fuelins_estimate
    """2 men needed working at 3*minwage minwage=8.21"""
    manhoursfoundation= num_bays*3*8.21

    foundation=foundationmaterials+equipment+manhoursfoundation
    """////////////////////////////////////////////////////////////////"""

    bayconstruct = num_bays*873.92
    """2 people 2 hours per bay"""
    manhoursconstruct = 2 * 2 * 3 * 8.21
    """each bay takes 2 hours"""
    equipmentconstruct = 2* 588/40 * num_bays +300 +60 +fuelins_estimate

    construct= bayconstruct+manhoursconstruct+equipmentconstruct
    """////////////////////////////////////////////////////////////////"""

    structurecost= foundation+construct+invertor
    return structurecost
