import sqlite3
from sqlite3 import Error


def db_write_user(conn: str, user: tuple) -> int:
    """Write a user to the database

    Args:
        conn (str): Connection to that database
        user (tuple): Must provide username and hash

    Returns:
        int: lastrowid
    """
    with sqlite3.Connection(conn) as connection:
        cursor = connection.cursor()
        sql = "INSERT INTO users (username, hash) VALUES (?, ?)"
        cursor.execute(sql, user)
        connection.commit()
        last = cursor.lastrowid
    return last


def db_get_users(conn: str, user: tuple) -> list:
    """Return all users, hash where the username matches (should be 1 or 0)

    Args:
        conn (str): Connection to the database
        user (tuple): username

    Returns:
        list: id, users, hash with the username provided
    """
    with sqlite3.Connection(conn) as connection:
        cursor = connection.cursor()
        sql = "SELECT id, username, hash FROM users WHERE username = ?"
        cursor.execute(sql, user)
        rows = cursor.fetchall()
    temp = [{"id":row[0],"name": row[1], "hash": row[2]} for row in rows]
    return temp