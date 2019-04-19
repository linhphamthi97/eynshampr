# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:04:16 2019

@author: neilw
"""
import matplotlib.pyplot as plt
import cashflowmodel2 
import numpy as np


netpresentvalue=[]

for j in range(1):
    netpresentvalue.append([])
    
    for i in np.linspace(150,210,4):
        netpresentvalue[j].append(cashflowmodel2.npv(i,0.32,1))
        
x = np.linspace(150,210,4)
plt.plot(x,netpresentvalue[0], '-b')

#plt.plot(netpresentvalue[2], '-g', label='0.23')

#plt.plot(netpresentvalue[4], '-c', label='0.25')

#plt.plot(netpresentvalue[6], '-k', label='0.27')
plt.title('IRR - no. bays installed')
plt.ylabel('IRR')
plt.xlabel('number of bays installed')      
plt.legend(loc='upper right')

#for i in range(0,8,2): 
max_value = max(netpresentvalue[0])
max_index = netpresentvalue[0].index(max_value)
print(max_index)



