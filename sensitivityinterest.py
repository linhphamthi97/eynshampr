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
import sensinterest
import numpy as np


netpresentvalue=[]

for j in range(1):
    netpresentvalue.append([])
    
    for i in np.linspace(0.05,0.15,11):
        netpresentvalue[j].append(sensinterest.npv(232,0.32,i))
        
x = np.linspace(5,15,11)
plt.plot(x,netpresentvalue[0], '-b')

#plt.plot(netpresentvalue[2], '-g', label='0.23')

#plt.plot(netpresentvalue[4], '-c', label='0.25')

#plt.plot(netpresentvalue[6], '-k', label='0.27')


plt.title('IRR - loan interest rate')
plt.ylabel('IRR')
plt.xlabel('Loan interest rate in percent')      
plt.legend(loc='upper right')
print(netpresentvalue[0])