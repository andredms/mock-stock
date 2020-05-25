##############################
# Purpose: Bot operations    #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 20/05/2020       #
##############################
from discord import Game
from dotenv import load_dotenv 
from discord.ext import commands, tasks

import pyimgur
import asyncio
import time
import sys
import discord
import os
import datetime

from getpercent import *
from updatedb import *
from graph import *
from database import *

load_dotenv()

#token goes here
TOKEN = 'x'

client = discord.Client()

##############################
# Name: on_ready             #
# Purpose: Changes status    #
# Import: None               #
##############################
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("ASX"))

##############################
# Name: on_message           #
# Purpose: Handles messages  #
# Import: User message       #
##############################
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    args = message.content.split()
    
    #INVEST
    if(message.content.startswith('$i')):
        await invest(message, args)
    #SELL
    if(message.content.startswith('$s')):
        await sell(message, args)
    #UPDATE
    if(message.content == '$u'):
        await update(message)
    #USER DETAILS
    if(message.content == '$p'):
        await profile(message)
    #ADDS USER TO DATABASE
    if(message.content == '$etup'):
        add_user(message.author.id, message.author.name)
        name = message.author.name
        embed = discord.Embed(title=name+ " has entered the market!", color=0xcc33ff)
        await message.channel.send(embed=embed)
    #HELP
    if(message.content == '$help'):
        embed = discord.Embed(title="MockStock Commands 🔎", color=0xcc33ff)
        embed.add_field(name="Add user", value="$etup", inline=False)
        embed.add_field(name="Invest", value="$i <company-acronym> <value>", inline=False)
        embed.add_field(name="Sell", value="$s <company-acronym>", inline=False)
        embed.add_field(name="Update", value="$u", inline=False)
        embed.add_field(name="Profile", value="$p", inline=False)
        await message.channel.send(embed=embed)

##############################
# Name: invest               #
# Purpose: allows investing  #
# Import: none               #
##############################
async def invest(message, args):
    #gets balance of a user
    balance = wrapper_select_balance(message.author.id)

    #assigns cmd lines args to variables for readability
    company = args[1]
    amount = round(float(args[2]), 2)

    has_invested = False
    is_company = False

    #gets current time
    now = datetime.datetime.now()  

    #works out if user has enough cash
    change = balance - amount

    #checks if user has already invested
    all_companies = wrapper_all_companies(message.author.id)
    if(company in all_companies):
        has_invested = True

    #checks if company is valid
    inc = getLink(company)
    if(inc != None or inc != '-'):
        is_company = True
    
    if((has_invested == False and is_company == True) and ((change >= 0.0) and (amount >= 0.10))):
            #format out message
            embed = discord.Embed(title="Invested 💰", description=message.author.mention + " invested in: " + company, color=0xcc33ff)
            embed.add_field(name="Amount", value="$" + str(amount), inline=False)

            wrapper_update_investments(message.author.id, company, amount, inc)
            wrapper_reduce_balance(message.author.id, float(amount))

            #if outside opening hours, set closing value to investment amount 
            if((now.hour < 8 and now.hour >= 14) and (change >= 0.0) and (amount >= 0.10)):
                wrapper_update_prev_value(message.author.id, company)
            await message.channel.send(embed=embed)
    #not enough money
    elif(change < 0):
        embed = discord.Embed(title="Insufficient funds!", color=0xff4545)
        await message.channel.send(embed=embed)
    #not large enough investment
    elif(amount < 0.10):
        embed = discord.Embed(title="Minimum investment: $0.10", color=0xff4545)
        await message.channel.send(embed=embed)
    #not a real company
    elif(is_company == False):
        embed = discord.Embed(title="That company doesn't exist!", color=0xff4545)
        await message.channel.send(embed=embed)
    #user has already invested
    elif(has_invested == True):
        embed = discord.Embed(title="You've already invested in " + list[1], description="Sell before buying more!", color=0xff4545)
        await message.channel.send(embed=embed)

##############################
# Name: sell                 #
# Purpose: allows selling    #
# Import: none               #
##############################
async def sell(message, args):
    #assignms cmd line arg to variable for readability 
    company = args[1]
    #gets all companies 
    all_companies = wrapper_all_companies(message.author.id)
    is_invested = False

    #checks if user has actually invested in company
    if company in all_companies:
            is_invested = True
    if(is_invested == True):
        #works out how much user will get back from selling share currently
        investment = investment_worth(message.author.id, company)
        curr_val = wrapper_select_curr_val(message.author.id, company)
        profit = curr_val - investment

        #takes company out of user's listings
        wrapper_withdraw(message.author.id, company)
        balance = wrapper_select_balance(message.author.id)

        #format message
        embed = discord.Embed(title="Sold 💸", description=message.author.mention + " withdrew: " + company, color=0xcc33ff)
        embed.add_field(name="Profit", value="$" + str(profit), inline=False)
        embed.add_field(name="Balance", value="$" + str(balance), inline=False)
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="You aren't a shareholder of " + company, color=0xff4545)
        await message.channel.send(embed=embed)

##############################
# Name: update               #
# Purpose: updates stocks    #
# Import: none               #
##############################
async def update(message):
    now = datetime.datetime.now()
    #if opening hours
    if((now.hour >= 8 and now.hour < 14)):
        embed = discord.Embed(title="Update 📈", color=0xcc33ff)
        all_companies = wrapper_all_companies(message.author.id)

        total_profit = 0
        new_profit = 0

        #FOR ALL COMPANIES INVESTED IN
        for company in all_companies:
            #get previous value
            prev_val = wrapper_select_prev(message.author.id, company)
            #get the increase in percent
            increase = float(getLink(company))
            #store raw percent
            rawIncrease = str(increase)
            increase = (increase / 100) + 1

            #new investments
            if(prev_val == 0.0):
                #get original worth
                investment = investment_worth(message.author.id, company)
                #get the starting increase
                starter_increase = (wrapper_select_start_precent(message.author.id, company) / 100)
                #get change in increase since first invested
                new_increase = increase - starter_increase
                #new current value
                curVal = investment * new_increase 

            #old investments
            else: 
                #new current value
                curVal = prev_val * increase
                #get initial investment value
                investment = investment_worth(message.author.id, company)

            #get the profit 
            profit = curVal - investment
            #add profit to total profits
            new_profit += profit
            profit = str(round(profit, 2))

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
            #update total profit of user
            wrapper_update_profit(message.author.id, new_profit)
            
        #profit with stocks currently held
        newProfit = str(round(newProfit, 2))
        if('-' in newProfit):
            newProfit.replace('-', '-$')
        else:
            newProfit = "$" + newProfit
        embed.add_field(name="Total Profit", value=newProfit, inline=False)
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Market is closed!", color=0xff4545)
        await message.channel.send(embed=embed)

##############################
# Name: update               #
# Purpose: updates stocks    #
# Import: none               #
##############################
async def profile(message):
    worth = 0.0

    #get balance of user
    balance = float(wrapper_select_balance(message.author.id))
    balance = round(balance, 2)

    #get all companies of user
    all_companies = wrapper_all_companies(message.author.id)
    companies = [None] * len(all_companies)
    for ii, company in enumerate(all_companies):
        companies[ii] = company + " ($" + str(float(round(wrapper_select_curr_val(message.author.id, company),2))) + ")"
        worth += float(wrapper_select_curr_val(message.author.id, company))

    #worth is current value of stocks + balance
    worth += balance
    worth = round(worth, 2)

    #get total profit of user
    profit = str(round(wrapper_select_profit(message.author.id), 2))

    #check for negative
    if('-' in profit):
        profit = profit.replace('-', '-$')
    else:
        profit = "$" + profit
    
    #format message
    embed = discord.Embed(title="Profile 👤", color=0xcc33ff)
    embed.add_field(name="Name", value=message.author.mention, inline=False)
    embed.add_field(name="Balance", value="$" + str(balance), inline=False)
    embed.add_field(name="Worth", value="$" + str(worth), inline=False)
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

    #embeds message in discord
    embed.set_image(url=image.link)

    await message.channel.send(embed=embed)

##############################
# Name: save_graph           #
# Purpose: sets closings     #
# Import: none               #
##############################
async def save_graph():
    await client.wait_until_ready()
    users = wrapper_select_users()
    #update users profits
    for id in users:
        worth = 0.0
        balance = 0.0

        #get all companies of user
        companies = wrapper_all_companies(id)
        for ii, company in enumerate(companies):
            worth += float(wrapper_select_curr_val(id, company))

        #get balance of user
        balance = round(wrapper_select_balance(id), 2)

        worth += float(balance)
        worth = round(worth, 2)

        filename = str(id) + '.txt'
        with open(filename, "a") as myFile:
            myFile.write(str(worth) + ',')

    #only happens every 24 hours
    await asyncio.sleep((60*60)*24)

#background task to continously set closing values/txt files for graphing
client.loop.create_task(save_graph())
client.run(TOKEN)
