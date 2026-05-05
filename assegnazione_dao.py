import sqlite3

def salva_assegnazione(id_richiesta, id_aula):
    conn = sqlite3.connect('db/assegnaAule.db')
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO assegnazione (id_richiesta, id_aula) VALUES (?, ?)"
        cursor.execute(sql, (id_richiesta, id_aula))
        conn.commit()
    except Exception as e:
        print("Errore nel salvataggio assegnazione:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def elimina_tutte_assegnazioni():
    """
    Pulisce la tabella assegnazione per ricalcolare da zero.
    """
    conn = sqlite3.connect('db/assegnaAule.db')
    cursor = conn.cursor()

    try:
        sql = "DELETE FROM assegnazione"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("Errore nella cancellazione assegnazioni:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_assegnazioni():
    """
    Restituisce tutte le assegnazioni salvate.
    """
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM assegnazione'
    cursor.execute(sql)
    assegnazioni = cursor.fetchall()

    cursor.close()
    conn.close()

    return assegnazioni
