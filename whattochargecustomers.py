# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:04:16 2019

@author: neilw
"""
import matplotlib.pyplot as plt
from cashflowmodel import npv
import operator



netpresentvalue=[]

for j in range(8):
    netpresentvalue.append([])
    
    for i in range(33):
        netpresentvalue[j].append(npv(i,j*0.01+0.17,1))
        

plt.plot(netpresentvalue[0], '-b', label='0.17')

plt.plot(netpresentvalue[2], '-g', label='0.19')

plt.plot(netpresentvalue[4], '-c', label='0.21')

plt.plot(netpresentvalue[6], '-k', label='0.23')
plt.title('NPV - no. structures installed')
plt.ylabel('NPV')
plt.xlabel('no. structures installed')      
plt.legend(loc='upper right')

for i in range(0,8,2): 
    max_value = max(netpresentvalue[0])
    max_index = netpresentvalue[0].index(max_value)
    print(max_index)



