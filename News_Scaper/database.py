import mysql.connector
import os
from dotenv import load_dotenv

# load file.env
load_dotenv()


# conect to the database
def connect_database():
    try:

        connection = mysql.connector.connect(
            host=os.getenv("DB_host"),
            user=os.getenv("DB_user"),
            password=os.getenv("DB_password"),
            database=os.getenv("DB_database"),
        )

        if connection.is_connected():
            print("sucessfull conection")
            return connection

    except mysql.connector.Error as e:
        print(f"error conecting to the  data base: {e}")


# functions to interact with the database
# variables to handle preference
connection = connect_database()
LIKE = 2
DISLIKE = 1


def insert_user(name, email):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(query, values)
    connection.commit()
    print("User inserted successfully")


def insert_keyword(user_id, keyword, preference):
    # handles preference errors
    preferences = [1, 2]
    if preference not in preferences:
        print("preference must be 1 or 2")  # 1 for dislike 2 for like
        return

    cursor = connection.cursor()
    query = "Insert into keywords (user_id,keyword,preference) values (%s,%s,%s)"
    values = (user_id, keyword, preference)
    cursor.execute(query, values)
    connection.commit()
    print("Key word inserted succesfully")


def insert_seen_news(user_id,title, link):
    cursor = connection.cursor()
    query = "Insert into seen_news (user_id,title,link) values (%s,%s,%s)"
    values = (user_id,title, link)
    cursor.execute(query, values)
    connection.commit()


def get_keywords(user_id_):
    cursor = connection.cursor()
    query = "select keyword ,preference from keywords where user_id = %s"
    cursor.execute(query, (user_id_,))
    key_list = cursor.fetchall()

    # exception error loading
    if key_list == None:
        print("error loading key words, or no keywords defined")
        return

    return key_list


def get_seen_titles(user_id_):
    cursor = connection.cursor()
    query = " select title from seen_news where user_id = %s"
    cursor.execute(query, (user_id_,))
    raw_data = cursor.fetchall()
    cursor.close()

    if not raw_data:
        return []

    return [row[0] for row in raw_data]


def get_all_users():
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  #
            query = "SELECT id, email, username FROM users"
            cursor.execute(query)

            users = cursor.fetchall()
            return users
        except mysql.connector.Error as e:
            print(f"Erro ao buscar utilizadores: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    return []


