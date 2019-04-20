# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:59:23 2019

@author: neilw
"""

#import matplotlib.pyplot as plt
#import pandas as pd
import matplotlib.pyplot as plt
from discountfactor import discountfactor
from income import income
from initialinvest import initial
from loanrepayment import fixedloanrepayment
import numpy as np
from maintain import annualmaintain
from replacement import replace

num_years = 30
selling_electricityprice=0.32
num_bays=342
"""data about car park"""
num_spaces=1000


""" data for economy """
inflation_cpi=0.02
cost_of_borrowing=0.055
discountpvwithtime=0.02333


loan_interest=0.1
loan_duration=20
#Preliminary    
discount=[]

#buying and selling electricity
#assuming same every year(no change in number of EVs)

cost_elec_buy=[]
cost_elec_sell=[]
"""yearly net cost sell - cost buy - loan repayment (- maintenance) etc."""
yearly_net=[]


initialinvest=initial(num_bays)

loan=int(initialinvest)+0.2*90000+57692
#loan repayment, first parameter is loan value, this will be changed iteratively so that npv never falls below zero for any year
repayment= fixedloanrepayment(loan,loan_interest,loan_duration)+[0]*(num_years-loan_duration)
#replacements
#hardcoded for 30 years
replacelist=[0]*9+[replace(num_bays)]
replacelist= replacelist*3

#replacement with discounting
pvdisc=[]
disc_replacelist=[]
for i in range(num_years):
    pvdisc.append((1-discountpvwithtime)**(i))
   
    disc_replacelist.append(replacelist[i]*pvdisc[i])

print("replacelist")
print(disc_replacelist)   
sellbuy=[[671737, 34812], [669863, 35351], [672483, 35172], [670333, 35028], [672089, 35289], [673676, 35519], [670410, 35747], [671753, 36087], [669169, 36049], [666288, 36198], [671737, 34812], [669863, 35351], [672483, 35172], [670333, 35028], [672089, 35289], [673676, 35519], [670410, 35747], [671753, 36087], [669169, 36049], [666288, 36198], [671737, 34812], [669863, 35351], [672483, 35172], [670333, 35028], [672089, 35289], [673676, 35519], [670410, 35747], [671753, 36087], [669169, 36049], [666288, 36198]]
#for years of operation
for j in range(num_years):
    cost_elec_buy.append(sellbuy[j][1])
    cost_elec_sell.append(sellbuy[j][0]*selling_electricityprice)


    #tallying
    
    yearly_net.append(cost_elec_sell[j]+income(num_spaces)-cost_elec_buy[j]-repayment[j]- annualmaintain(num_bays) -disc_replacelist[j])

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
print("loan/minumum working capital")
print(-1*min(accumulated_discount))
print(loan)
print("irr")
irr=np.irr(yearly_net)
print(irr)

x = range(2020,2051)
plt.figure()
plt.plot(x,accumulated_discount, '-b')
#plt.plot(netpresentvalue[6], '-k', label='0.27')
plt.title('Accumulated discounted cash flow with time')
plt.ylabel('Accumulate DCF')
plt.xlabel('Year')      
plt.legend(loc='upper right')


plt.figure()

plt.plot(x,discounted_yearly_net, '-b')
#plt.plot(netpresentvalue[6], '-k', label='0.27')
plt.title('Annual discounted cash flow with time')
plt.ylabel('Annual DCF')
plt.xlabel('Year')      
plt.legend(loc='upper right')