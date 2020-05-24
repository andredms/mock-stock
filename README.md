# MockStock
![](https://i.imgur.com/9P3PAQI.png)
                                             
                                             
A fake stock market which utilises Python, SQLite and Selenium. Allows users to invest into the ASX without the risk of losing any money. Scrapes the ASX through a Chrome web-driver, getting real-time increases/decreases and stores all investor data within a database which the user can query through various commands. The market is open on weekdays 5am - 3pm (WAST) and closes on weekends, users can still invest and use the bot outside of these hours, however their profits won't go up until the market re-opens. 

Ideal for a Discord server as it allows users to compete with friends. There's also a simple CLI version (not uploaded) if you want to run solo. Leaderboards and 24/7 hosting coming soon!

## Usage
#### Host
```python3 bot.py```

#### Create Database
```python3 database.py```

#### List Commands
```$help```

#### Add Profile to Database 
 ```$etup```

All users inititally start out with $500 spending cash, they can invest this and then sell their stocks to earn more money. 

#### View Profile
```$p```

This command brings up how much a user is worth, the profit they've made on the ASX, their invested companies and an embeded graph of their profits over time. Graph is scheduled to update every 24 hours.

#### Invest
```$i <company-acronym> <amount>```
  
Allows the user to invest into a company. If you've already invested in a company, you must sell all your shares in it before buying extra (eventually will be able to invest new amounts into the same company). 
  
#### Sell
```$s <company-name>```
  
Sells all shares a user holds for any given company (eventually will be able to sell a given amount).
  
#### Update
```$u```

Updates the values of a shareholders stocks and displays the new value of them. This can be done at any time during opening hours. 
