##############################
# Purpose: Create database   #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 21/05/2020       #
##############################
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_stockholder(conn, user):
    sql = ''' INSERT INTO users(id, name, worth, profit)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_db():
    create_connection(r"stocks.db")
    database = (r"stocks.db")

    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    worth REAL,
                                    profit REAL
                                ); """

    sql_create_company_table = """ CREATE TABLE IF NOT EXISTS companies (
                                       userId INTEGER,
                                       company TEXT,
                                       invested REAL,
                                       curValue REAL,
                                       prevValue REAL,
                                       startPercent REAL,
                                       FOREIGN KEY(userId) REFERENCES users(id)
                             ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_company_table)
    else:
        print("Error: cannot create database connection")

def add_user(userId, username):
    database = (r"stocks.db")
    conn = create_connection(database)
    with conn:
        user = (userId, username, "500.0", "0.0")
        user_id = create_stockholder(conn, user)

create_db()