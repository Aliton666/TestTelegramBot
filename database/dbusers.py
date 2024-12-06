import sqlite3
from core.config import *

# Подключение к базе данных
connection = sqlite3.connect('appointments.db')


def check_users(user_id):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY,\
        user_id BIGINT,\
        username VARCHAR(45) DEFAULT NULL,\
        first_name VARCHAR(255) DEFAULT NULL,\
        last_name VARCHAR(255) DEFAULT NULL,\
        phone VARCHAR(255) DEFAULT NULL,\
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")

    check = cursor.fetchone()
    if check is not None:
        return check
    else:
        return None


def registration_users(user_id, username, first_name, last_name, phone):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY,\
    user_id BIGINT,\
    username VARCHAR(45) DEFAULT NULL,\
    first_name VARCHAR(255) DEFAULT NULL,\
    last_name VARCHAR(255) DEFAULT NULL,\
    phone VARCHAR(255) DEFAULT NULL,\
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("INSERT INTO users(user_id, username, first_name, last_name, phone)\
        VALUES(?, ?, ?, ?, ?)", (user_id, username, first_name, last_name, phone))
    connection.commit()
    cursor.close()


def add_procedure(name, description):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO procedures (name, description)
        VALUES (?, ?)
    """, (name, description))
    connection.commit()


def create_tables():
    cursor = connection.cursor()
    
    # Таблица процедур
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS procedures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
    """)

    # Таблица специалистов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specialists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    # Таблица времени
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id BIGINT,
            procedure_id INTEGER,
            specialist_id INTEGER,
            appointment_date DATE,
            appointment_time TIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (procedure_id) REFERENCES procedures (id),
            FOREIGN KEY (specialist_id) REFERENCES specialists (id)
        )
    """)
    
    connection.commit()



def add_specialist(name):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO specialists (name)
        VALUES (?)
    """, (name,))
    connection.commit()

def get_procedures():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM procedures")
    return cursor.fetchall()

def get_specialists():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialists")
    return cursor.fetchall()

def create_appointment(user_id, procedure_id, specialist_id, appointment_date, appointment_time):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO appointments (user_id, procedure_id, specialist_id, appointment_date, appointment_time)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, procedure_id, specialist_id, appointment_date, appointment_time))
    connection.commit()
    cursor.close()
