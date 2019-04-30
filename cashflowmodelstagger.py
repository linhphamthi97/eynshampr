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

    


def npv(num_bayz,selling_electricityprice,dt):
    
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

    
    #buying and selling electricity
    #assuming(no change in number of EVs
    #num bays to be installed linear increase
    #sellbuy=listsellbuy(10,0.965,0.993125,0.1807,num_bayz,dt)
    sellbuy=[[669541, 36671], [664431, 36657], [663012, 36424], [666815, 37109], [666308, 36785], [663959, 37035], [663782, 37503], [661451, 37221], [656414, 38117], [660006, 38369], [671656, 35107], [671834, 35434], [672638, 35379], [671224, 35340], [673236, 35575], [669907, 35487], [673312, 35986], [667458, 35805], [669366, 35973], [668255, 36356], [676070, 35186], [671640, 35096], [673404, 35078], [671294, 35507], [674479, 35494], [671694, 35536], [670452, 35151], [672620, 35952], [670016, 35711], [666825, 36535]]

    cost_elec_buy=[]
    cost_elec_sell=[]
    """yearly net cost sell - cost buy - loan repayment (- maintenance) etc."""

    
    yearly_net=[]
    

    initialinvest=initial(num_bayz,0)+57692
    
    
    loan=int(initialinvest)+0.2*90000
    
    #loan repayment, first parameter is loan value, this will be changed iteratively so that npv never falls below zero for any year
    

    
    num_bays=num_bayz
    
    cost_elec_buy=[]
    cost_elec_sell=[]
    discount=[]
    yearly_net=[]

    
    repayment= fixedloanrepayment(loan,loan_interest,loan_duration)+[0]*11
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
    print(yearly_net[1])
    print(cost_elec_sell[0])
    print(cost_elec_sell)
    print(income(num_spaces))
    print(cost_elec_buy[0])
    print(repayment[0])
    print(annualmaintain(num_bays))
    print(replacelist[0])
    print(cost_elec_sell[0]+income(num_spaces)-cost_elec_buy[0]-repayment[0]- annualmaintain(num_bays) -replacelist[0])

    
    #discounting 
    
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
            if yearly_net[i]<=0:
                taxpaid.append(0)
                taxloss=taxloss+discounted_yearly_net[i]    
                 #tax=======
            elif yearly_net[i]>0:
                            
                if discounted_yearly_net[i]+taxloss>0:
                            #tax 0.17
                    taxpaid.append((discounted_yearly_net[i]+taxloss)*0.17)
                    yearly_net[i]=yearly_net[i]-(discounted_yearly_net[i]+taxloss)*0.17
                    discounted_yearly_net[i]=yearly_net[i]*discount[i]
                    taxloss=0
                 
                else:
                    taxpaid.append(0)
                    taxloss=discounted_yearly_net[i]+taxloss
            
                #==========    
            accumulated_discount.append(discounted_yearly_net[i]+accumulated_discount[i-1])


        

    
    print(yearly_net)
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
    print(taxpaid)
    return accumulated_discount

#print(numpy.irr(annualbalance))



#listsellbuy(10,0.965,0.993125,0.1807,100,0.25)

#npv(100,0.32,0.25)
