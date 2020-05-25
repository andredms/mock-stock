##############################
# Purpose: Graphs earnings   #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 20/05/2020       #
##############################
import matplotlib.pyplot as plt
from pylab import figure, axes, pie, title, show
import numpy as np
import os

def graph(userId, username):
    plt.style.use('seaborn-whitegrid')
    filename = str(userId) + '.txt'

    #gets csv from file
    x = np.genfromtxt(filename, delimiter=',')
    y = [None] * len(x)
    for ii, coordinates in enumerate(x):
            y[ii] = coordinates
            x[ii] = ii

    plt.suptitle(username + "\'s Worth", fontsize=20)
    plt.ylabel('Amount ($)')
    plt.xlabel('Days')
    plt.axhline(y=500, color='b', linestyle='--')
    plt.plot(x, y, color="red")
    out = str(userId) + '.png'
    #os.remove(out)
    plt.savefig(out)