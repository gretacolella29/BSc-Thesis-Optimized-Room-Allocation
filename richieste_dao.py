import sqlite3

def get_richieste():
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM richiesta'
    cursor.execute(sql)
    richieste = cursor.fetchall()

    cursor.close()
    conn.close()

    return richieste

def get_richiesta_by_id(id):
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM richiesta WHERE id = ?'
    cursor.execute(sql, (id,))
    richiesta = cursor.fetchone()

    cursor.close()
    conn.close()

    return richiesta

# In richieste_dao.py

def get_richieste_by_idProf(idProf):
    """
    Restituisce tutte le richieste effettuate da uno specifico professore.
    """
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM richiesta WHERE idProf = ?'
    cursor.execute(sql, (idProf,))
    richieste = cursor.fetchall()

    cursor.close()
    conn.close()

    return richieste


def create_richiesta(idProf, capienza, slots, giorno, prese, pc, proiettore):
    slot_str = ",".join(map(str, slots))

    conn = sqlite3.connect('db/assegnaAule.db')
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO richiesta (idProf, capienza, slots, giorno, prese, pc, proiettore)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (idProf, capienza, slot_str, giorno, prese, pc, proiettore))
        conn.commit()
    except Exception as e:
        print("Errore inserimento richiesta:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()




