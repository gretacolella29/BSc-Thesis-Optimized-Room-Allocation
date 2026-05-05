from flask_login import UserMixin

class Aula:
    def __init__(self, id_aula, capienza, prese, pc, proiettore):
        self.id_aula = id_aula
        self.capienza = capienza
        self.prese = prese
        self.pc = pc
        self.proiettore = proiettore

    def __str__(self):
        return f"Aula {self.id_aula} - Capienza: {self.capienza}"

class User(UserMixin):
    def __init__(self, id, nome, cognome, email, password):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password

    def __str__(self):
        return f"Prof. {self.nome} {self.cognome} - Email: {self.email}"


class Richiesta:
    def __init__(self, id, id_prof, capienza_richiesta, slotIds, giorno,  prese, pc, proiettore):
        """
        slot_ids: lista di ID degli slot richiesti (es. [2, 3, 4] se serve un blocco di 3 slot)
        """
        self.id = id
        self.id_prof = id_prof
        self.capienza_richiesta = capienza_richiesta
        self.slotIds = slotIds  # ad es. [2, 3] se occupa due fasce orarie
        self.giorno = giorno
        self.prese = prese
        self.pc = pc
        self.proiettore = proiettore

    def __str__(self):
        return (f"Richiesta {self.id} di Prof. {self.id_prof}, "
                f"capienza: {self.capienza_richiesta}, slot_ids: {self.slotIds}")



class Slot:
    def __init__(self, id, ora_inizio, ora_fine):
        self.id = id
        
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine

    def __str__(self):
        return (f"Slot {self.id} - "
                f"{self.ora_inizio}-{self.ora_fine}")
