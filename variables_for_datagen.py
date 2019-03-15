# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:54:47 2019

@author: Nicole
"""

#%% LENGTH OF STAY
#2nd method
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

#mu = 10
#sigma = 2.1
#x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
#plt.plot(x, stats.norm.pdf(x, mu, sigma))
#plt.title('Distribution representing length of stay in P&R')
#plt.ylabel('Probability')
#plt.xlabel('Time parked (hours)')
#
#plt.show()

time = np.random.normal(10,2.1)
print(time)

#%% EV BATTERY CAPACITY

# From report, typical capacities (all Li-ion batteries) are:

#corresponding to Renault Twizzy, Hyundai Ioniq, Nissan Leaf, VW E-Golf, Tesla Model S
capacity = [6.1,6.1,28,28,28,28,28,28,28,28,28,28,30,30,30,30,30,30,30,30,30,30,24.2,24.2,24.2,24.2,24.2,24.2,24.2,24.2,24.2,24.2,100,100,100]
bins = 100
plt.figure()
plt.hist(capacity, bins, normed=True, histtype='bar')

x = np.linspace(0, 120, 100) #range of kWh 

## lets try the normal distribution first
#mu, sigma = stats.norm.fit(capacity) # get mean and standard deviation
#pdf_g = stats.norm.pdf(x,mu,sigma) # now get theoretical values in our interval  
#plt.plot(x, pdf_g, label="Normal") # plot it

# gamma dist - best
ag,bg,cg = stats.gamma.fit(capacity)  
pdf_gamma = stats.gamma.pdf(x,ag,bg,cg)  
plt.plot(x, pdf_gamma)

## beta dist
#ab,bb,cb,db = stats.beta.fit(capacity)  
#pdf_beta = stats.beta.pdf(x,ab,bb,cb,db)  
#plt.plot(x, pdf_beta, label="Beta")

plt.title('Distribution of popular EV battery capacities')
plt.xlabel('kWh')
plt.ylabel('Probability')
plt.legend()
plt.show()

# clearly gamma distribution fits best
# mu = 32kWh from Sam's data
# shape = sqrt(mu), scale = shape
shape, scale = 5.66,7
capacity = np.random.gamma(shape, scale)

#%% SOC on arrival

# use EV battery capacity distribution

#mu = 18
#sigma = 3
#x = np.linspace(2, 30, 100)
#pdf_g = stats.norm.pdf(x,mu,sigma)
#plt.plot(x, pdf_g)
#plt.title('Distribution representing distance travelled to P&R')
#plt.ylabel('Probability')
#plt.xlabel('Distance (miles)')
#
#plt.show()
#
#plt.figure()
#consumption = 0.293 #kWh/mile
#SOC = [(i - mu*consumption)/i for i in capacity] #assuming all travelling 4 miles
##print(SOC)
#
#bins = 50
#plt.hist(SOC, bins, normed=1, histtype='bar')
#x = np.linspace(0,1,100)
#
##ag,bg,cg  = stats.gamma.fit(SOC)  
##pdf_gamma = stats.gamma.pdf(x,ag,bg,cg)  
##plt.plot(x,pdf_gamma,label='Gamma')
#
#ab,bb,cb,db = stats.beta.fit(SOC)  
#pdf_beta = stats.beta.pdf(x,ab,bb,cb,db)  
#plt.plot(x,pdf_beta,label='Beta')
#
#a, b = 2, 1.7
#SOC = np.random.beta(a,b)
#
#plt.title('Distribution of SOC on arrival')
#plt.xlabel('Proportion of charge')
#plt.ylabel('Frequency')
#plt.legend()

#%% Arrival time

x = range(0,25)
y = pd.read_csv('Arrivaltime.csv', usecols=[1])
totalcars = 617
arrival = y.values/totalcars
plt.figure()
plt.plot(x,arrival)
plt.title('Distribution of influx of cars')
plt.xlabel('Time of day (hour)')
plt.ylabel('Number of cars')

import seaborn as sns
n = 10000 # number of samples to be drawn
mu = [9, 17] # mean of each normal distribution (i.e. the peaks)
sigma = [0.1,2.1] # standard deviation of each dist which allows best fit of Pear Tree data
samples = []
for i in range(n): # iteratively draw samples
    Z = np.random.choice([0,1]) # latent variable
    samples.append(np.random.normal(mu[Z], sigma[Z], 1))
sns.distplot(samples, hist=False) # compare plot with Pear Tree
plt.show()

# extracting one random sample to give arrivaltime input

n = 1 # extract one sample
mu = [9, 17]
sigma = [0.1,2.1]
Z = np.random.choice([0,1]) # latent variable
arrivaltime = float(np.random.normal(mu[Z], sigma[Z], 1))
print(arrivaltime)