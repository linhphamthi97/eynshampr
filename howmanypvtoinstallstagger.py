# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:04:16 2019

@author: neilw
"""
import matplotlib.pyplot as plt
import cashflowmodelstagger 
import numpy as np


netpresentvalue=[]

for j in range(1):
    netpresentvalue.append([])
    
    for i in np.linspace(232,232,1):
        netpresentvalue[j].append(cashflowmodelstagger.npv(i,0.32,1))
        
x = np.linspace(2020,2050,31)
plt.plot(x,netpresentvalue[0], '-b')

#plt.plot(netpresentvalue[2], '-g', label='0.23')

#plt.plot(netpresentvalue[4], '-c', label='0.25')

#plt.plot(netpresentvalue[6], '-k', label='0.27')
plt.title('IRR - no. bays installed')
plt.ylabel('IRR')
plt.xlabel('number of bays installed')      
plt.legend(loc='upper right')




