##############################
# Purpose: Bot operations    #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 20/05/2020       #
##############################
import os
import discord
from dotenv import load_dotenv
import random
from getpercent import *
import sys
from updatedb import *
import datetime
from database import *
from graph import *
import schedule
import time
from discord.ext import commands, tasks
import asyncio
import pyimgur

load_dotenv()
TOKEN = 'x'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    list = message.content.split()
    now = datetime.datetime.now()

    #SET CLOSING VALUES
    if(now.hour > 15 and now.hour < 23):
        companies = wrapper_all_companies(message.author.id)
        for company in companies:
            wrapper_update_prev_value(message.author.id, company)
        profit = wrapper_select_profit(message.author.id)

    #INVEST
    if(message.content.startswith('$i')):
        worth = wrapper_select_worth(message.author.id)
        hasInvested = False
        found = True
        amount = float(list[2])
        amount = round(amount, 2)
        change = worth - amount
        now = datetime.datetime.now()
        companies = wrapper_all_companies(message.author.id)
        for ii in companies:
            if(ii == list[1]):
                hasInvested = True

        inc = getLink(list[1])
        if(inc == None or inc == '-'):
            found = False
        
        if(hasInvested == False and found == True):
            #opening hours
            if((now.hour > 5 and now.hour < 15)and (change >= 0) and (amount >= 0.10) and (now.day >= 1 and now.day <= 5)):
                wrapper_update_investments(message.author.id, list[1], amount, float(inc))
                wrapper_reduce_worth(message.author.id, float(amount))
                embed = discord.Embed(title="Invested 💰", description=message.author.mention + " invested in: " + list[1], color=0xcc33ff)
                embed.add_field(name="Amount", value="$" + str(amount), inline=False)
                await message.channel.send(embed=embed)

            #not during opening hours
            elif(change >= 0 and amount >= 0.10):
                embed = discord.Embed(title="Invested 💰", description=message.author.mention + " invested in: " + list[1], color=0xcc33ff)
                embed.add_field(name="Amount", value="$" + str(amount), inline=False)
                wrapper_update_investments(message.author.id, list[1], amount, 0.0)
                await message.channel.send(embed=embed)
                wrapper_reduce_worth(message.author.id, float(amount))
            #not enough money
            elif(change < 0):
                embed = discord.Embed(title="Insufficient funds!", color=0xff4545)
                await message.channel.send(embed=embed)
            elif(amount < 0.10):
                embed = discord.Embed(title="Minimum investment: $0.10", color=0xff4545)
                await message.channel.send(embed=embed)
        elif(found == False):
            embed = discord.Embed(title="That company doesn't exist!", color=0xff4545)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="You've already invested in " + list[1], description="Sell before buying more!", color=0xff4545)
            await message.channel.send(embed=embed)
    
    #SELL STOCKS
    if(message.content.startswith('$s')):
        companies = wrapper_all_companies(message.author.id)
        found = False
        if list[1] in companies:
                found = True
        if(found == True):
            #work out profit 
            profit = wrapper_select_curr_val(message.author.id, list[1]) - investment_worth(message.author.id, list[1])

            #format message
            embed = discord.Embed(title="Sold 💸", description=message.author.mention + " withdrew: " + list[1], color=0xcc33ff)
            embed.add_field(name="Profit", value="$" + str(profit), inline=False)
            await message.channel.send(embed=embed)

            #remove company from user
            wrapper_withdraw(message.author.id, list[1])
        else:
            embed = discord.Embed(title="You aren't a shareholder of " + list[1], color=0xff4545)
            await message.channel.send(embed=embed)

    #UPDATE STOCK VALUES
    if(message.content.startswith('$u')):
        now = datetime.datetime.now()
        if((now.hour > 5 and now.hour < 15) and (now.day >= 1 and now.day <= 5)):
            list = wrapper_all_companies(message.author.id)
            totalProfit = 0
            newProfit = 0
            embed = discord.Embed(title="Update 📈", color=0xcc33ff)

            #FOR ALL COMPANIES INVESTED IN
            for company in list:
                #get previous value
                prevVal = wrapper_select_prev(message.author.id, company)

                #get the increase in percent
                increase = float(getLink(company))

                #store raw percent
                rawIncrease = str(increase)

                increase = (increase / 100) + 1

                #IF NEW INVESTMENT
                if(prevVal == 0.0):
                    #get original worth
                    investment = investment_worth(message.author.id, company)

                    #get the starting increase
                    starterIncrease = (wrapper_select_start_precent(message.author.id, company) / 100)

                    #get change in increase since first invested
                    newIncrease = increase - starterIncrease

                    #new current value
                    curVal = investment * newIncrease 

                    #get the profit 
                    profit = str((curVal - investment))

                    #add profit to total profits
                    newProfit += float(profit)
                    profit = float(profit)
                    profit = round(profit, 2)
                    profit = str(profit)

                    #check if profit is negative
                    if('-' in profit):
                        profit = profit.replace('-', '-$')
                    else:
                        profit = "$" + profit
                    if('-' in str(rawIncrease)):
                        embed.add_field(name=company, value="Down: " + rawIncrease + "%" + " (" + profit + ")", inline=False)
                    else:
                        embed.add_field(name=company, value="Up: " + rawIncrease + "%" + " (" + profit + ")", inline=False)

                    #update new value
                    wrapper_update_curr_val(message.author.id, curVal, company)
                #old investments
                else: 
                    #new current value
                    curVal = prevVal * increase

                    #get initial investment value
                    investment = investment_worth(message.author.id, company)

                    #add profit to total profits
                    profit = float(curVal - investment)
                    newProfit += profit
                    profit = round(profit, 2)
                    profit = str(profit)

                    #check if profit is negative
                    if('-' in profit):
                        profit.replace('-', '-$')
                    else:
                        profit = "$" + profit
                    if(('-' in str(rawIncrease))):
                        embed.add_field(name=company, value="Down: " + rawIncrease + " (" + profit + ")", inline=False)
                    else:
                        embed.add_field(name=company, value="Up: " + rawIncrease + "%" + " (" + profit + ")", inline=False)   
                    
                    #update new value
                    wrapper_update_curr_val(message.author.id, curVal, company)

                #update total profit of user
                wrapper_update_profit(message.author.id, newProfit)

            newProfit = round(newProfit, 2)
            newProfit = str(newProfit)
            if('-' in newProfit):
                newProfit.replace('-', '-$')
            else:
                newProfit = "$" + newProfit
            embed.add_field(name="Total Profit", value=newProfit, inline=False)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Market is closed!", color=0xff4545)
            await message.channel.send(embed=embed)

    #USER DETAILS
    if(message.content.startswith('$p')):
        #get all companies of user
        companies = wrapper_all_companies(message.author.id)
        for ii, company in enumerate(companies):
            companies[ii] = company + " ($" + str(wrapper_select_curr_val(message.author.id, company)) + ")"

        #get worth of user
        worth = wrapper_select_worth(message.author.id)
        worth = round(worth, 2)
        worth = str(worth)

        #get total profit of user
        profit = str(wrapper_select_profit(message.author.id))

        #format message
        embed = discord.Embed(title="Profile 👤", color=0xcc33ff)
        embed.add_field(name="Name", value=message.author.mention, inline=False)
        embed.add_field(name="Worth", value="$" + worth, inline=False)

        #check for negative
        if('-' in profit):
            profit = profit.replace('-', '-$')

        embed.add_field(name="Toal Profit", value=profit, inline=False)

        embed.add_field(name="Companies", value=companies, inline=False)

        #generates graph with matplotlib and saves to .png named after userId
        graph(message.author.id, message.author.name)

        #get .png graph
        filename = str(message.author.id) + '.png'

        #for pyimgur
        CLIENT_ID = "x"
    
        #uploads to imgur from local 
        im = pyimgur.Imgur(CLIENT_ID)

        #gets link of imgur upload
        image = im.upload_image(filename)
        embed.set_image(url=image.link)
        await message.channel.send(embed=embed)
        
    #ADDS USER TO DATABASE
    if(message.content == '$etup'):
        add_user(message.author.id, message.author.name)
        name = message.author.name
        embed = discord.Embed(title=name+ " has entered the market!", color=0xcc33ff)
        await message.channel.send(embed=embed)
    
    if(message.content == '$help'):
        embed = discord.Embed(title="MockStock Commands 🔎", color=0xcc33ff)
        embed.add_field(name="Add user", value="$etup", inline=False)
        embed.add_field(name="Invest", value="$i <company-acronym> <value>", inline=False)
        embed.add_field(name="Sell", value="$s <company-acronym>", inline=False)
        embed.add_field(name="Update", value="$u", inline=False)
        embed.add_field(name="Profile", value="$p", inline=False)
        await message.channel.send(embed=embed)


async def saveGraph():
    await client.wait_until_ready()
    users = wrapper_select_users()
    for id in users:
        profit = wrapper_select_profit(id)
        filename = str(id) + '.txt'
        with open(filename, "a") as myFile:
            myFile.write(str(profit) + ',')
    #only happens every 24 hours
    await asyncio.sleep((60*60)*24)

client.loop.create_task(saveGraph())
client.run(TOKEN)