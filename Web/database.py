import pymysql.cursors
import pandas as pd
from config import mysql_host, mysql_user, mysql_password, mysql_db

def get_db_connection():
    connection = pymysql.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        db=mysql_db,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def Customer():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_name FROM customer"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def Product_score():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product_score'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()
        
def Recommend():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM recommend'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def Purchase():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM purchase'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def Product():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()
