# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:19:28 2019

@author: neilw
"""
import matplotlib.pyplot as plt
import sensitivityanalysisinstallationcost
import numpy as np


netpresentvalue=[]

for j in range(1):
    netpresentvalue.append([])
    
    for i in np.linspace(0.9,1.1,21):
        netpresentvalue[j].append(sensitivityanalysisinstallationcost.npv(232,0.32,i))
        
x = np.linspace(90,110,21)
plt.plot(x,netpresentvalue[0], '-b')

#plt.plot(netpresentvalue[2], '-g', label='0.23')

#plt.plot(netpresentvalue[4], '-c', label='0.25')

#plt.plot(netpresentvalue[6], '-k', label='0.27')


plt.title('IRR - purchase, delivery and installation cost')
plt.ylabel('IRR')
plt.xlabel('Percentage of purchase, delivery and installation cost')      
plt.legend(loc='upper right')
print(netpresentvalue[0])