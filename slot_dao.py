import sqlite3

def get_slot_id_by_label( ora_inizio, ora_fine):
    
    ora_inizio = ora_inizio.strip()
    ora_fine = ora_fine.strip()

    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = """
        SELECT id FROM slot
        WHERE  ora_inizio = ? AND ora_fine = ?
    """
    cursor.execute(sql, ( ora_inizio, ora_fine))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    

    return row['id'] if row else None


def get_slot_by_id(slot_id):
    """
    Restituisce il singolo slot dato il suo ID.
    """
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM slot WHERE id = ?'
    cursor.execute(sql, (slot_id,))
    slot = cursor.fetchone()

    cursor.close()
    conn.close()

    return slot

def get_descrizione_slot_by_ids(slot_ids):
    """
    Riceve una lista di ID slot e restituisce una descrizione leggibile.
    """
    descrizioni = []
    for slot_id in slot_ids:
        slot = get_slot_by_id(slot_id)
        if slot:
           
            ora_inizio = slot['ora_inizio']
            ora_fine = slot['ora_fine']
            descrizioni.append(f" {ora_inizio}-{ora_fine}")
    return ", ".join(descrizioni)


def get_all_slots():
    """
    Restituisce tutti gli slot esistenti nel database.
    """
    conn = sqlite3.connect('db/assegnaAule.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM slot'
    cursor.execute(sql)
    slots = cursor.fetchall()

    cursor.close()
    conn.close()

    return slots
