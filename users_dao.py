import sqlite3
from models import User

def get_users():
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id FROM users'
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

def add_user(user):

    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO user(nome, cognome, email, password) VALUES(?,?,?,?)' 

    try:
        print(user)
        
        cursor.execute(
            sql, (user['nome'], user['cognome'],user['email'],user['password'],))  
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_user_by_email(email):
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM user WHERE email = ?'
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user_by_id(id):
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM user WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
