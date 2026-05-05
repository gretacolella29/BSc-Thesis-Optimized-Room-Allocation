import sqlite3

def get_aule():

    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM aula'
    cursor.execute(sql)
    aule = cursor.fetchall()

    cursor.close()
    conn.close()

    return aule

def get_aula_by_id(id):

    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM aula WHERE id = ? '
    cursor.execute(sql, (id,))
    aula = cursor.fetchone()

    cursor.close()
    conn.close()

    return aula