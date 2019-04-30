# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:38:09 2019

@author: neilw
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:19:28 2019

@author: neilw
"""
import matplotlib.pyplot as plt
import demandsens
import numpy as np


netpresentvalue=[]

for j in range(1):
    netpresentvalue.append([])
    
    for i in np.linspace(0.9,1.15,21):
        netpresentvalue[j].append(demandsens.npv(232,0.32,i))
        
x = np.linspace(90,115,21)
plt.plot(x,netpresentvalue[0], '-b')

#plt.plot(netpresentvalue[2], '-g', label='0.23')

#plt.plot(netpresentvalue[4], '-c', label='0.25')

#plt.plot(netpresentvalue[6], '-k', label='0.27')


plt.title('IRR - Percentage of estimated EV charging turnover')
plt.ylabel('IRR')
plt.xlabel('Percentage of estimated EV charging turnover')      
plt.legend(loc='upper right')
print(netpresentvalue[0])