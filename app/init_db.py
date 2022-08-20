import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import extensions

def get_create_database_query():
    return "CREATE DATABASE social"

try:
    postgres_connection = psycopg2.connect(host="localhost", user="leo", 
    password="psw", cursor_factory=RealDictCursor)
    postgres_connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = postgres_connection.cursor()
    cursor.execute(get_create_database_query())
    print("Eeemotional Damage Dodged! 😋😎")

except Exception as exception:
    print("💥 Emotional Damage!", exception)