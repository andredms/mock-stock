##############################
# Purpose: Graphs earnings   #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 20/05/2020       #
##############################
import matplotlib.pyplot as plt
from pylab import figure, axes, pie, title, show
import numpy as np

def graph(userId, username):
    plt.style.use('seaborn-whitegrid')
    filename = str(userId) + '.txt'

    #gets csv from file
    x = np.genfromtxt(filename, delimiter=',')
    y = [None] * len(x)
    for ii, coordinates in enumerate(x):
        if(ii == 0):
            y[ii] == coordinates
        elif(coordinates != y[ii - 1]):
            y[ii] = coordinates

    plt.suptitle(username + "\'s earnings", fontsize=20)
    plt.ylabel('Amount ($)')
    plt.xlabel('Days')
    plt.axhline(y=0, color='b', linestyle='--')
    plt.plot(y, x, color="red")
    out = str(userId) + '.png'
    plt.savefig(out)