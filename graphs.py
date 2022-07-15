# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 21:09:26 2021

@author: Patrik
"""

import pandas as pd

df = pd.read_csv ('simulation_results.csv')

x1 = df.loc[df['type'] == "h_1"]
x1 = (x1['count'].sum() / x1.shape[0])

x2 = df.loc[df['type'] == "h_2"]
x2 = (x2['count'].sum() / x2.shape[0])

x3 = df.loc[df['type'] == "l_2"]
x3 = (x3['count'].sum() / x3.shape[0])

df = pd.DataFrame({'Trajectories':['fixed', 'currents - 100 x 100', 'currents - 10 x 10'], 'Amount of trash':[x1, x2, x3]})
ax = df.plot.bar(x='Trajectories', y='Amount of trash', rot=0)