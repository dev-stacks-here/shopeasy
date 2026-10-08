# db.py  -  small helper functions to talk to MySQL.
# app.py calls these so that it does not repeat connection code everywhere.

import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Open a new connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=()):
    """Run a SELECT query and return ALL rows as a list of dictionaries."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)    # dictionary=True -> row["pname"]
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def fetch_one(sql, params=()):
    """Run a SELECT query and return only ONE row (or None if nothing found)."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def execute(sql, params=()):
    """Run INSERT / UPDATE / DELETE, save the change, return the new id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()                  # commit = make the change permanent
    new_id = cursor.lastrowid      # id given to a newly inserted row
    cursor.close()
    conn.close()
    return new_id
