##############################
# Purpose: Run features      #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 21/05/2020       #
##############################
from getpercent import *
import sys
from updatedb import *
import datetime

now = datetime.datetime.now()

#investing in new companies 
if(len(sys.argv) > 3):
    worth = wrapper_select_worth()
    change = worth - float(sys.argv[3])
    if(sys.argv[1] == "-i" and change >= 0):
        if(now.hour > 5 and now.hour < 13):
            wrapper_update_investments(sys.argv[2], sys.argv[3], float(getLink(sys.argv[2])))
        else:
            wrapper_update_investments(sys.argv[2], sys.argv[3], 0.0)
        print("-----------------------------------------------------")
        print("Invested: " + sys.argv[2] + ", " + sys.argv[3])
        print("-----------------------------------------------------")
        wrapper_reduce_worth(float(sys.argv[3]))
    elif(sys.argv[1] == "-i" and change < 0):
        print("-----------------------------------------------------")
        print("Insufficient funds!")
        print("-----------------------------------------------------")
#withdrawing investment from company - initial investment amount + profit
elif(sys.argv[1] == "-w"):
    wrapper_withdraw(sys.argv[2])
    print("-----------------------------------------------------")
    print("Withdrawn: " + sys.argv[2])
    print("-----------------------------------------------------")
#set closing values for next day - this will eventually be automated when running 24/7
elif(sys.argv[1] == "-s"):
    if(now.hour > 13 and now.hour < 23):
        list = wrapper_all_companies()
        for company in list:
            wrapper_update_prev_value(company)
        print("-----------------------------------------------------")
        print("Closing values set! See you tomorrow.")
        print("-----------------------------------------------------")
    else:
        print("-----------------------------------------------------")
        print("Market is open! Can't set closing values.")
        print("-----------------------------------------------------")
#updates investment values - this will eventually be automated when running 24/7
elif(sys.argv[1] == "-u"):
    if(now.hour > 5 and now.hour < 13):
        list = wrapper_all_companies()
        totalProfit = 0
        newProfit = 0
        for company in list:
            increase = float(getLink(company))
            increase = (increase / 100) + 1
            prevVal = wrapper_select_prev(company)
            #new daily investments, this condition is for stocks bought in the middle of the day
            #if something is up 11%, you can't invest $10 and have it automatically go up $11.1
            if(prevVal == 0.0):
                investment = investment_worth(company)
                starterIncrease = (wrapper_select_start_precent(company) / 100)
                newIncrease = increase - starterIncrease
                curVal = investment * newIncrease 
                newProfit += curVal - investment
                wrapper_update_curr_val(curVal, company)
            #old investments
            else:                
                curVal = prevVal * increase
                investment = investment_worth(company)
                newProfit += curVal - investment
                wrapper_update_curr_val(curVal, company)
            print("Your " + company + " investment is now worth: $" + str(curVal))
            print("-----------------------------------------------------")
        print("PROFIT: $" + str(newProfit))
        print("-----------------------------------------------------")
        wrapper_update_profit(newProfit)
    else:
        print("-----------------------------------------------------")
        print("Markets are closed!")
        print("-----------------------------------------------------")
#get profile details
elif(sys.argv[1] == "-d"):
    print("-----------------------------------------------------")
    print("HOWL")
    print(".....................................................")
    print("Worth: " + str(wrapper_select_worth()))  
    print("Profit: " + str(wrapper_select_profit()))
    list = wrapper_all_companies()
    print("Companies: ", end="")
    for company in list:
        print(company + " ", end="")
    print("")
    print("-----------------------------------------------------")
