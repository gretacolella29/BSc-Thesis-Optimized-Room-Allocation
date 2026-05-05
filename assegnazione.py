def assegna_aula(richiesta, lista_aule):
    # Filtra le aule che soddisfano la capienza richiesta
    aule_adatte = [aula for aula in lista_aule 
                   if aula.capienza >= richiesta.capienza_richiesta]
    
    if not aule_adatte:
        # Nessuna aula ha capienza sufficiente
        return None
    
    # Tra le aule che soddisfano il requisito, scegli quella con capienza minore
    aula_assegnata = min(aule_adatte, key=lambda x: x.capienza)
    return aula_assegnata

def assegna_aule_multi_slot(richieste, aule, slots):
    """
    Assegna un'aula a quante più richieste possibili, tenendo conto di:
    - capienza (>= capienza richiesta)
    - disponibilità su TUTTI gli slot richiesti (nessuna sovrapposizione)
    
    Ritorna un dizionario id_richiesta -> (id_aula assegnata o None).
    """
    # 1. Ordina le richieste per capienza crescente (puoi anche inserire altri criteri)
    richieste_ordinate = sorted(richieste, key=lambda r: r.capienza_richiesta)
    
    # 2. Ordina le aule per capienza crescente
    aule_ordinate = sorted(aule, key=lambda a: a.capienza)
    
    # 3. Inizializza disponibilità per (aula, slot) =  chiave
    disponibilita = {}
    for aula in aule_ordinate:
        for slot in slots:
            disponibilita[(aula.id_aula, slot.idSlot)] = True #chiave del dizionario sono idaula, idslot
    
    # 4. Dizionario dei risultati
    assegnazioni = {}
    
    # 5. Assegnazione
    for richiesta in richieste_ordinate:
        aula_trovata = None
        
        # Proviamo a cercare tra le aule in ordine di capienza
        for aula in aule_ordinate:
            if aula.capienza >= richiesta.capienza_richiesta:
                # Controlliamo che TUTTI gli slot della richiesta siano disponibili per questa aula
                tutti_slot_liberi = True
                for id_slot_richiesto in richiesta.slotIds:
                    if not disponibilita[(aula.id_aula, id_slot_richiesto)]:
                        tutti_slot_liberi = False
                        break
                
                # Se tutti gli slot sono liberi, abbiamo trovato l'aula
                if tutti_slot_liberi:
                    aula_trovata = aula
                    break
        
        # Se abbiamo trovato un'aula disponibile, la assegniamo e impostiamo la disponibilità a False
        if aula_trovata:
            assegnazioni[richiesta.id_richiesta] = aula_trovata.id_aula
            for id_slot_richiesto in richiesta.slotIds:
                disponibilita[(aula_trovata.id_aula, id_slot_richiesto)] = False
        else:
            # Nessuna aula adatta
            assegnazioni[richiesta.id_richiesta] = None
    
    return assegnazioni
