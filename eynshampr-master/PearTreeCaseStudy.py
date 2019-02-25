# -*- coding: utf-8 -*-
"""

"""
import matplotlib.pyplot as plt
import pandas as pd
labels=['Time','Percentage Occupied']
xls = pd.ExcelFile('C:/Users/neilw/Desktop/3rd Year Engineer/3YP/FirstOrderModel/FirstOrderModelStats.xlsx')
df = pd.read_excel(xls, 'PercentageOccupiedTime', names=labels)

plt.plot(df['Time'],df['Percentage Occupied'])
plt.xlabel(labels[0])
plt.ylabel(labels[1])