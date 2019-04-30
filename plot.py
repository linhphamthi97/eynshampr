# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:44:20 2019

@author: neilw
"""
import matplotlib.pyplot as plt
import numpy as np
#import numpy as np


x = np.linspace(90,110,5)
#npv_y=[-607036.524, 98392.34676620414, 94423.637455981, 91643.68781997186, 89481.77751609439, 87080.97145262395, 83909.30483252743, 81154.52199274229, 78512.28057773443, 74626.97889731728, -633094.3281679201, 74907.63901775534, 72538.4671646758, 70563.8815855363, 68230.22047675583, 66403.78783471155, 63894.916221543346, 62259.04909993945, 59538.84335761849, 57931.269577234794, -567996.2635768133, 88300.19549588536, 85000.6068457121, 82610.5694412358, 79594.74408710285, 77517.68362585099, 74737.61581653048, 72388.06711264762, 70072.14455650644, 67656.69321527977, 69083.2531351083]
y=[0.0865,0.0795,0.072,0.065,0.0585]
z=[0.08,0.076,0.072,0.067,0.062]
k=[0.033,0.053,0.072,0.096,0.12]
plt.plot(x,y, '-k', label='Purchase, Delivery and Installation')
plt.plot(x,z, '-g', label='Loan Interest Rate')
plt.plot(x,k,'-b',label='EV Turnover')
#plt.plot(netpresentvalue[4], '-c', label='0.25')

#plt.plot(netpresentvalue[6], '-k', label='0.27')
plt.title('IRR - Percentage of estimated value')
plt.ylabel('IRR')
plt.xlabel('Percentage of estimated value')      
plt.legend(loc='upper right')