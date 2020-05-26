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
    #removes duplicates, this won't be needed when hosted 24/7
    x = list(dict.fromkeys(x))

    y = np.arange(1, len(x) + 1, 1)

    plt.suptitle(username + "\'s Worth", fontsize=20)
    plt.ylabel('Amount ($)')
    plt.xlabel('Days')
    plt.axhline(y=500, color='b', linestyle='--')
    plt.plot(y, x, color="red")
    out = str(userId) + '.png'
    plt.savefig(out)
    plt.close()