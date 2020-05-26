##############################
# Purpose: Update database   #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 20/05/2020       #
##############################
import sqlite3
from sqlite3 import Error

#standard method to connect to database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

#get the worth of someone
def select_balance(conn, id):
    cur = conn.cursor()
    balance = cur.execute("SELECT balance FROM users WHERE id=?", (id,))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#get the total profit of someone
def select_profit(conn, id):
    cur = conn.cursor()
    profit = cur.execute("SELECT profit FROM users WHERE id=?", (id,))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#get investment worth
def select_investment_val(conn, userId, company):
    cur = conn.cursor()
    investment = cur.execute("SELECT invested FROM companies WHERE userId=? AND company=?", (userId,company,))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#get current value of share of company for user
def select_curr_val(conn, userId, company):
    cur = conn.cursor()
    curr_val = cur.execute("SELECT curValue FROM companies WHERE userId=? AND company=?", (userId,company,))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#get previous closing value
def select_prev_val(conn, userId, company):
    cur = conn.cursor()
    prev_val = cur.execute("SELECT prevValue FROM companies WHERE userId=? AND company=?", (userId,company,))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#gets list of all companies user is invested in
def select_all_companies(conn, userId):
    cur = conn.cursor()
    all_companies = cur.execute("SELECT company FROM companies WHERE userId=?", (userId,))
    rows = cur.fetchall()
    all_companies = []
    for row in rows:
        all_companies.append(row[0])
    return all_companies

#gets list of all users
def select_users(conn):
    cur = conn.cursor()
    users = cur.execute("SELECT id FROM users")
    rows = cur.fetchall()
    users_all = []
    for row in rows:
        users_all.append(row[0])
    return users_all

#gets previous closing value of a user's investment for a specific company
def select_prev_value(conn, userId, company):
    cur = conn.cursor()
    prev_val = cur.execute("SELECT prevValue FROM companies WHERE userId=? AND company=?", (userId,company))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#gets the value of what the increase/decrease % was when user first invested
def select_start_percent(conn, userId, company):
    cur = conn.cursor()
    start_percent = cur.execute("SELECT startPercent FROM companies WHERE userID=? AND company=?", (userId, company))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

#update someone's total profit
def update_profit(conn, task):
    sql = ''' UPDATE users
              SET profit = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

#update someone's balance
def update_balance(conn, task):
    sql = ''' UPDATE users
              SET balance = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

#update current value of users share
def update_cur_val(conn, task):
    sql = ''' UPDATE companies
              SET curValue = ?
              WHERE userId = ? AND company = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

#sets the closing values at 3pm
def update_prev_value(conn, task):
    sql = ''' UPDATE companies
              SET prevValue = ?
              WHERE userId = ? AND company = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

#invest in a new company
def update_investments(conn, task):
    sql = ''' INSERT INTO companies(company, invested, userID, curValue, prevValue, startPercent)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

#adds users
def create_stockholder(conn, user):
    sql = ''' INSERT INTO users(id, name, balance, profit)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

#withdraw company from someone's investments 
def withdraw_company(conn, company, userId):
    cur = conn.cursor()
    sql = ''' DELETE FROM companies WHERE company = ? AND userId = ?'''
    cur = conn.cursor()
    cur.execute(sql, (company, userId,))
    conn.commit()

def wrapper_select_balance(userId):
    database = r"stocks.db"
    conn = create_connection(database)
    balance = select_balance(conn, userId)
    return balance

def wrapper_reduce_balance(userId, val):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        balance = select_balance(conn, userId)
        balance = balance - val
        update_balance(conn, (balance, userId))

def wrapper_update_investments(userId, company, invested, startPercent):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        update_investments(conn, (company, invested, userId, invested, 0.0, startPercent))

def wrapper_withdraw(userId, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        cashback = select_curr_val(conn, userId, company)
        withdraw_company(conn, company, userId)
        balance = select_balance(conn, userId)
        balance = balance + cashback
        update_balance(conn, (balance, userId))
        
def wrapper_all_companies(userId):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        all_companies = select_all_companies(conn, userId)
    return all_companies

def wrapper_select_curr_val(userId, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        curVal = select_curr_val(conn, userId, company)
    return curVal

def wrapper_update_curr_val(userId, curVal, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        curVal = update_cur_val(conn, (curVal, userId, company))
    
def wrapper_update_profit(userId, profit):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        update_profit(conn, (profit, userId))

def wrapper_update_prev_value(userId, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        curValue = select_curr_val(conn, userId, company)
        update_prev_value(conn, (curValue, userId, company))

def wrapper_select_prev(userId, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        prevValue = select_prev_val(conn, userId, company)
    return prevValue

def investment_worth(userId, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
            investment = select_investment_val(conn, userId, company)
    return investment

def wrapper_select_profit(userId):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        profit = select_profit(conn, userId)
    return profit

def wrapper_select_start_precent(userId, company):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        startPercent = select_start_percent(conn, userId, company)
    return startPercent

def wrapper_select_users():
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        users = select_users(conn)
    return users

def add_user(userId, username):
    database = (r"stocks.db")
    conn = create_connection(database)
    balance = "500.0"
    with conn:
        user = (userId, username, balance, "0.0")
        user_id = create_stockholder(conn, user)

def wrapper_increase_balance(userId, bal_increase):
    database = r"stocks.db"
    conn = create_connection(database)
    with conn:
        curr_balance = select_balance(conn, userId)
        new_balance = curr_balance + bal_increase
        print(bal_increase)
        update_balance(conn, (bal_increase, userId))