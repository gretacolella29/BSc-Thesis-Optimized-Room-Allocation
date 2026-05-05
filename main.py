from models import Aula, User, Richiesta, Slot
import assegnazione as ass

def main():
    # 1. Creiamo i 35 slot (5 giorni × 7 fasce)
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    fasce = [
        ("08:30", "10:00"),
        ("10:00", "11:30"),
        ("11:30", "13:00"),
        ("13:00", "14:30"),
        ("14:30", "16:00"),
        ("16:00", "17:30"),
        ("17:30", "19:00")
    ]
    
    slots = []
    slot_id = 1
    for giorno in giorni:
        for (start, end) in fasce:
            slots.append(Slot(slot_id, giorno, start, end))
            slot_id += 1

    # 2. Creiamo alcune aule
    aule = [
        Aula(1, 20),
        Aula(2, 40),
        Aula(3, 60),
        Aula(4, 100),
    ]

    
    # 3. Creiamo professori (opzionale ai fini della logica)
    professori = [
        User(101, "Mario", "Rossi", "m.rossi@example.com", "pwd1"),
        User(102, "Luca", "Bianchi", "l.bianchi@example.com", "pwd2"),
    ]
    
    # 4. Creiamo richieste con liste di slot
    #   Per esempio: (8:30-10:00) e (10:00-11:30) => slot_id=1 e slot_id=2
    #   Sotto ipotizziamo che i docenti richiedano da 1 a 2 slot consecutivi
    richieste = [
        Richiesta(1001, 101, 15, [1]),        # Un solo slot (Lunedì 08:30-10:00)
        Richiesta(1002, 101, 30, [1, 2]),     # Due slot consecutivi (08:30-11:30)
        Richiesta(1003, 102, 40, [2, 3]),     # (10:00-13:00) -> 2 slot
        Richiesta(1004, 102, 60, [2, 3]),     # Stesso blocco di 1003, competono
        Richiesta(1005, 101, 20, [8]),        # Martedì 08:30-10:00
        Richiesta(1006, 102, 50, [8, 9]),     # Martedì 08:30-11:30
    ]
    
    # 5. Assegnazione
    assegnazioni = ass.assegna_aule_multi_slot(richieste, aule, slots)
    
    # 6. Stampa i risultati
    for richiesta in richieste:
        aula_ass = assegnazioni[richiesta.id_richiesta]
        print(f"Richiesta {richiesta.id_richiesta} (cap={richiesta.capienza_richiesta}, slot={richiesta.slotIds}) -> {aula_ass}")

if __name__ == "__main__":
    main()
