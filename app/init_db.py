from sqlite3 import connect
from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        postgres_connection = psycopg2.connect(host="localhost", database="", 
        user="leo", password="psw", cursor_factory=RealDictCursor, autocommit=True)
        cursor = postgres_connection.cursor() 
        print("Connected to DB! ⚡")
        break

    except Exception as exception:
        print("💥 Failed to connect to DB!", exception)
        sleep(2)

cursor.execute("""CREATE DATABASE social""")
postgres_connection.commit()

cursor.execute("""CREATE TABLE posts ()""")
print("DB Created! ✔")
