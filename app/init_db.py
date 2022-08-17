from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor

def get_create_database_query():
    return "CREATE DATABASE social"

def get_create_posts_table_query():
    return """CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        content VARCHAR(500) NOT NULL,
        published boolean NOT NULL DEFAULT true,
        created_on TIMESTAMP NOT NULL DEFAULT NOW())"""

def get_insert_post_test_query(title, content):
    return f"""INSERT INTO posts (
        title,
        content
    ) VALUES (
        {title},
        {content}
    )"""

def get_test_query():
    return """SELECT * FROM posts"""


try:
    with psycopg2.connect(host="localhost", database="social", user="leo", 
    password="psw", cursor_factory=RealDictCursor) as postgres_connection:
        
        postgres_connection.autocommit = True
        with postgres_connection.cursor() as cursor:

            cursor.execute(get_create_posts_table_query())
            cursor.execute(get_test_query())
            print("Not Eeemotional Damage! 😋😎")

except Exception as exception:
    print("💥 Emotional Damage!", exception)
    sleep(2)
