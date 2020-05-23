# MockStock
A fake stock market which utilises Python, SQLite, Selenium and Matplotlib. Allows users to invest into the ASX without the risk of losing any money. Scrapes the ASX through a Chrome web-driver and stores all investor data stored within a database which the user can query through various commands. The market is open on weekdays 5am - 3pm (WAST) and closes on weekends, users can still invest and use the bot outside of these hours, however their profits won't go up until the market re-opens. 

## Usage
#### List Commands
$help

#### Add Profile to Database 
$etup

All users inititally start out with $500 spending cash, they can invest this and then sell their stocks to earn more money. 

#### View Profile
$p 

This command brings up how much a user is worth, the profit they've made on the ASX, their invested companies and an embeded graph of their profits over time. Graph is scheduled to update every 24 hours.

#### Invest
$i <company-acronym> <amount>
  
Allows the user to invest into a company. 
  
#### Sell
$s <company-name>
  
Sells all shares a user holds for any given company (eventually will be able to sell a given amount).
  
#### Update
$u

Updates the values of a shareholders stocks and displays the new value of them. This can be done at any time during opening hours. 
