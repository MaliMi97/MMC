import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(''))
from TASEPv3 import *
from DataProcessing_v3 import *

def get_result(tasep, p, parametres, start):    # returns an array of tuples (density, particle flow density, alpha, beta)
    res = []
    for j in parametres:
        print(j)
        for k in parametres:
            d = DataProcessing(tasep.execute(p, j, k))
            aux = d.get_result(start)
            res.append((aux[0], aux[1], j, k))
    return np.array(res)

def plot_header(xlabel, ylabel): # sets size, labels and font of 2d graph
    font = 30
    plt.figure(figsize=(15,10))
    plt.xticks(fontsize=font)
    plt.yticks(fontsize=font)
    plt.xlabel(xlabel, fontsize=font, loc='right')
    plt.ylabel(ylabel, fontsize=font, rotation=0, loc='top')

def plot_result_alpha(res, variable, variable_index, param): # auxiliary function for plotting 2d results with fixed beta
    plot_header(r'$\alpha$', variable)
    for i in param:
        plt.plot(param, res[res[:,3]==i][:,variable_index], label=r'$\beta=$'+f'{i:.2f}')
    plt.legend(prop={'size': 15}, bbox_to_anchor=(1.05, 1), loc='upper left')
    
def plot_result_beta(res, variable, variable_index, param): # auxiliary function for plotting 2d results with fixed alpha
    plot_header(r'$\beta$', variable)
    for i in param:
        plt.plot(param, res[res[:,2]==i][:,variable_index], label=r'$\alpha=$'+f'{i:.2f}')
    plt.legend(prop={'size': 15}, bbox_to_anchor=(1.05, 1), loc='upper left')
    
def plot_result(res, param): # plots results
    plot_result_alpha(res, r'$\rho\,$[m$^{-1}$]', 0, param)
    plot_result_alpha(res, r'$J\,$[s$^{-1}$]', 1, param)
    plot_result_beta(res, r'$\rho\,$[m$^{-1}$]', 0, param)
    plot_result_beta(res, r'$J\,$[s$^{-1}$]', 1, param)
    
def plot_compare(res_par, res_ran): # compares the two models
    plot_header(r'$\rho\,$[m$^{-1}$]', r'$J\,$[s$^{-1}$]')
    plt.plot(res_par[:,0], res_par[:,1], '.r', label='parallelní schéma')
    plt.plot(res_ran[:,0], res_ran[:,1], '.', label='schéma s náhodným pořadím')
    plt.legend(prop={'size': 15}, bbox_to_anchor=(1.05, 1), loc='upper left')
