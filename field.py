# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 17:06:08 2021

@author: Patrik
"""

import numpy as np
import matplotlib.pyplot as plt

grid_resolution = 100
def matrix_combinator(a,b):
    result =  []
    for i in range(len(a)):
        row = []
        for j in range(len(a[i])):
            row.append([0,0])
        result.append(row)
    
    for i in range(len(a)):
        for j in range(len(a[i])):
            result[i][j] = [a[i][j][0]+b[i][j][0], a[i][j][1]+b[i][j][1]]
    return result

def gyre_generator(dimensions, old_matrix):
    r = dimensions
    c = dimensions

    original_row = 5
    original_column = 10
    
    r2 = int(r/original_row)
    c2 = int(r/original_column)

    matrix = [] 

    for i in range(original_row):
        a =[] 
        for j in range(original_column):
            for k in range(c2):
                a.append(old_matrix[i][j]) 
    
        for l in range(r2):
            matrix.append(a)
    return matrix


gyre2 = [
            [[1,1],[1,0],[1,1],[1,1],[0,1],[1,1],[1,1],[1,0],[1,1],[0,1]],
            [[1,-1],[1,-1],[1,0],[1,0],[1,1],[1,1],[1,1],[0,1],[1,1],[0,1]],
            [[0,-1],[1,-1],[1,-1],[1,-1],[1,0],[0,0],[-1,0],[-1,1],[-1,1],[-1,1]],
            [[1,-1],[0,-1],[0,-1],[-1,-1],[-1,0],[-1,-1],[-1,-1],[-1,-1],[-1,1],[-1,1]],
            [[0,-1],[0,-1],[-1,-1],[-1,-1],[-1,0],[-1,-1],[-1,-1],[-1,0],[-1,-1],[-1,-1]],
        ]
        
combined_gyre = matrix_combinator(gyre2, gyre2)
scaled_gyre = gyre_generator(grid_resolution, combined_gyre)

x,y = np.meshgrid(np.linspace(0,10,10),np.linspace(0,5,5))

u1 = []
u2 = []

u = []
v = []

for i in gyre2:
    for j in i:
        u.append(j[0])
        v.append((-1*j[1]))
        
plt.gca().invert_yaxis()
plt.rcParams["figure.figsize"]=(20, 20)
plt.quiver(x,y,u,v)
plt.show()