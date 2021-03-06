# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:10:31 2019

@author: neilw
"""
#import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
from energydemand import energydemand
from discountfactor import discountfactor
from energydeficit import energydeficit
from income import income
from itertools import chain
from panelstructurecost import structurecost
from loanrepayment import fixedloanrepayment
from operator import add
from pvsystemcost import pvsystemcost

def npv(num_PVstructure,selling_electricityprice,staggerpart1,staggerpart2):

    num_years = 30
    
    
    """data about car park"""
    num_spaces=1000
    num_PVperstructure=7*3*num_PVstructure
    proportionEV=0.01
    efficiencyPV=0.197
    maintenance = 1000 * num_PVstructure
    
    """ data for economy """
    inflation_electricity=0.02
    inflation_rpi=0.024
    cost_of_borrowing=0.05 
    discountpvwithtime=0.01
    
    
    loan_interest=0.05
    loan_duration=10
    #Preliminary
    buying_electricitycost=0.17
    cost_freight= 100
    
    discount=[]
    
    #buying and selling electricity
    #assuming same every year(no change in number of EVs)
    cost_elec_buy=[]
    cost_elec_sell=[]
    """yearly net cost sell - cost buy - loan repayment (- maintenance) etc."""
    yearly_net=[]
    
    
    
    elec_buy=list(chain.from_iterable([-sum(energydeficit(num_PVperstructure,efficiencyPV,proportionEV))]*(num_years+1)))
    elec_sell=list(chain.from_iterable([sum(energydemand(proportionEV))]*(num_years+1)))
    
    duration_structure = loan_duration+staggerpart1-2
    duration_pvsystem = loan_duration+staggerpart2-2    
    repayment_structure = fixedloanrepayment(structurecost(num_PVstructure),loan_interest,loan_duration,staggerpart1,cost_freight,0)+[0]*(num_years-duration_structure)
    repayment_pvsystem = fixedloanrepayment(pvsystemcost(num_PVstructure),loan_interest,loan_duration,staggerpart2,cost_freight,discountpvwithtime)+[0]*(num_years-duration_pvsystem)
 
    repayment=list(map(add,repayment_structure,repayment_pvsystem))
 
    for j in range(len(elec_buy)):
        cost_elec_buy.append(elec_buy[j]*buying_electricitycost)
        cost_elec_sell.append(elec_sell[j]*selling_electricityprice)
        yearly_net.append(cost_elec_sell[j]+income(num_spaces)-cost_elec_buy[j]-repayment[j]- maintenance)
            
    
    
    
    #discounting and tallying
    """not discounted properly"""
    discounted_yearly_net=[]
    accumulated_discount=[]
    for i in range(num_years+1):
        discount.append(discountfactor(cost_of_borrowing,inflation_rpi,i))
        
        discounted_yearly_net.append(yearly_net[i]*discount[i])
        if i==0:
            accumulated_discount.append(discounted_yearly_net[i])
        else:
            accumulated_discount.append(discounted_yearly_net[i]+accumulated_discount[i-1])
        
    print("discounted yearly net")
    
    print(discounted_yearly_net)
    print("accumulated discount")
    
    print(accumulated_discount)
    
    npv= sum(discounted_yearly_net)
    print("npv")
    print(npv)

    return npv

#print(numpy.irr(annualbalance))

