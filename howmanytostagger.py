# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:04:16 2019

@author: neilw
"""
import matplotlib.pyplot as plt
from cashflowmodel import npv



netpresentvalue=[]

for j in range(5):
    netpresentvalue.append([])
    
    for i in range(30):
        netpresentvalue[j].append(npv(i,0.25,1,j+1))
        

plt.plot(netpresentvalue[0], '-b', label='1')

plt.plot(netpresentvalue[1], '-g', label='2')

plt.plot(netpresentvalue[2], '-c', label='3')

plt.plot(netpresentvalue[3], '-k', label='4')

plt.plot(netpresentvalue[4], '-y', label='5')

plt.title('NPV - no. structures installed')
plt.ylabel('NPV')
plt.xlabel('no. structures installed')      
plt.legend(loc='upper right')

for i in range(0,8,2): 
    max_value = max(netpresentvalue[0])
    max_index = netpresentvalue[0].index(max_value)
    print(max_index)

