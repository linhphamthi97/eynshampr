# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:10:31 2019

@author: neilw
"""
import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
from discountfactor import discountfactor
from income import income
from initialinvest import initial
from loanrepayment import fixedloanrepayment
import main
from maintain import annualmaintain
from replacement import replace

#lifespan=10
#eff_decfirst=0.965
#eff_dec=0.993125
#start_eff=0.1807
#bays=100
#dt=0.25
# 10 year lifespan of solar pv
# building an extra bays number of bays at each replacement and replacing old bays
def listsellbuy(lifespan,eff_decfirst,eff_dec,start_eff,bays,dt):
    lifespan = lifespan
    start_eff= start_eff
    eff_dec=eff_dec
    bays=bays
    i=0
    eff = start_eff
    listsellbuy = []
    while i<lifespan:
        if i==1:
            eff=eff*eff_decfirst
        else:
            eff=eff*eff_dec**i
        if listsellbuy==None or listsellbuy=="": 
            pass
        main.variable(eff,bays,dt)
        listsellbuy.append(main.results())
        
        i+=1
    i=0
    while i<lifespan:
        if i==1:
            eff=eff*eff_decfirst
        else:
            eff=eff*eff_dec**i
        if listsellbuy==None or listsellbuy=="": 
            pass
        main.variable(eff,2*bays,dt)
        listsellbuy.append(main.results())
        
        i+=1
    i=0
    while i<lifespan:
        if i==1:
            eff=eff*eff_decfirst
        else:
            eff=eff*eff_dec**i
        if listsellbuy==None or listsellbuy=="": 
            pass
        main.variable(eff,3*bays,dt)
        listsellbuy.append(main.results())
        
        i+=1
    

    print(listsellbuy)
    return listsellbuy

    


def npv(num_bays,selling_electricityprice,dt):

    num_years = 30
    
    
    """data about car park"""
    num_spaces=1000

    
    """ data for economy """
    inflation_cpi=0.02
    cost_of_borrowing=0.055
    #discountpvwithtime=0.02333
    
    
    loan_interest=0.1
    loan_duration=20
    #Preliminary    
    discount=[]
    
    #buying and selling electricity
    #assuming(no change in number of EVs
    #num bays to be installed linear increase
    sellbuy=listsellbuy(10,0.965,0.993125,0.1807,num_bays,dt)
    cost_elec_buy=[]
    cost_elec_sell=[]
    """yearly net cost sell - cost buy - loan repayment (- maintenance) etc."""

    
    yearly_net=[]
    

    initialinvest=initial(num_bays,0)
    
    loan=int(initialinvest)+0.2*80000+57692
    #loan repayment, first parameter is loan value, this will be changed iteratively so that npv never falls below zero for any year
    repayment= fixedloanrepayment(loan,loan_interest,loan_duration)+[0]*(num_years-loan_duration)
#replacements
    #hardcoded for 30 years
    replacelist=[0]*9+[replace(num_bays,10)]+[0]*9+[replace(num_bays,20)]+[0]*9+[0]
   

    #replacement with discounting
    
 #for years of operation
    for j in range(num_years):
        capital=0
        if j==10:
            num_bays=2*num_bays
        elif j==9:
            capital=initial(num_bays,j+1)
        elif j==20:
            num_bays=1.5*num_bays
        elif j==19:    
            capital=initial(num_bays,j+1)
        cost_elec_buy.append(sellbuy[j][1])
        cost_elec_sell.append(sellbuy[j][0]*selling_electricityprice)
        


        #tallying
        
        yearly_net.append(cost_elec_sell[j]+income(num_spaces)-cost_elec_buy[j]-repayment[j]- annualmaintain(num_bays) -replacelist[j] -capital)
        
#include zeroth year no loan
    zeroth=-initialinvest
    
    yearly_net=[zeroth]+yearly_net
   
    
    #discounting 
    """not discounted properly"""
    #apply discount factor
    discounted_yearly_net=[]
    #running total
    accumulated_discount=[]
    
   
    taxpaid=[]
    taxloss=0
    for i in range(num_years+1):
        discount.append(discountfactor(cost_of_borrowing,inflation_cpi,i))
        
        discounted_yearly_net.append(yearly_net[i]*discount[i])
        
        if i==0:
            accumulated_discount.append(discounted_yearly_net[i])
            taxpaid.append(0)
        #AIA will surpass all income therefore no tax paid in this year
        elif i%10==0:
            taxpaid.append(0)
            accumulated_discount.append(discounted_yearly_net[i]+accumulated_discount[i-1])
            
        else:           
            if discounted_yearly_net[i]<=0:
                taxpaid.append(0)
                taxloss=taxloss+discounted_yearly_net[i]    
                 #tax=======
            elif discounted_yearly_net[i]>0:
                            
                if discounted_yearly_net[i]+taxloss>0:
                            #tax 0.17
                    taxpaid.append((discounted_yearly_net[i]+taxloss)*0.17)
                    discounted_yearly_net[i]=discounted_yearly_net[i]-(discounted_yearly_net[i]+taxloss)*0.17
                    taxloss=0
                 
                else:
                    taxpaid.append(0)
                    taxloss=discounted_yearly_net[i]+taxloss
            
                #==========    
            accumulated_discount.append(discounted_yearly_net[i]+accumulated_discount[i-1])
            
        
    print("discounted yearly net")
 
    print(discounted_yearly_net)
    print("accumulated discount")
    
    print(accumulated_discount)
    
    npv= sum(discounted_yearly_net)
    print("npv")
    print(npv)
    print("irr")
    irr=np.irr(yearly_net)
    print(irr)
    print("loan/minumum working capital")
    print(-1*min(accumulated_discount))
    print(loan)
    print(taxpaid)
    return irr

#print(numpy.irr(annualbalance))



#listsellbuy(10,0.965,0.993125,0.1807,100,0.25)

#npv(100,0.32,0.25)
