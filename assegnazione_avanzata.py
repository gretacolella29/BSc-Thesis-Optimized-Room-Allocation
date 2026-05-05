# Nuovo algoritmo avanzato per assegnare aule
import aule_dao

giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]

def assegna_aule_avanzato(richieste, aule, slots):
    disponibilita = {}
    for aula in aule:
        for giorno in giorni:
            for slot in range(1, 8):  # ID slot da 1 a 7
                disponibilita[(aula.id_aula, giorno, slot)] = True

    alternative_per_richiesta = {}
    for richiesta in richieste:
        alternative = 0
        for aula in aule:
            if aula.capienza >= richiesta.capienza_richiesta:
                if all(disponibilita[(aula.id_aula, richiesta.giorno, id_slot)] for id_slot in richiesta.slotIds):
                    alternative += 1
        alternative_per_richiesta[richiesta.id] = alternative

    richieste_ordinate = sorted(richieste, key=lambda r: (alternative_per_richiesta[r.id], r.capienza_richiesta))

    assegnazioni = {}
    motivazioni = {}

    for richiesta in richieste_ordinate:
        aula_trovata = None
        max_match = -1
        aule_ordinate = sorted(aule, key=lambda a: a.capienza)

        for aula in aule_ordinate:
            if aula.capienza >= richiesta.capienza_richiesta:
                if all(disponibilita[(aula.id_aula, richiesta.giorno, id_slot)] for id_slot in richiesta.slotIds):
                    aula_db = aule_dao.get_aula_by_id(aula.id_aula)
                    if not aula_db:
                        continue

                    match = (
                        (richiesta.prese and aula_db['prese']) +
                        (richiesta.pc and aula_db['pc']) +
                        (richiesta.proiettore and aula_db['proiettore'])
                    )
                    if match > max_match:
                        aula_trovata = aula
                        max_match = match

        if aula_trovata:
            assegnazioni[richiesta.id] = aula_trovata.id_aula
            motivazioni[richiesta.id] = "Assegnazione diretta"
            for id_slot in richiesta.slotIds:
                disponibilita[(aula_trovata.id_aula, richiesta.giorno, id_slot)] = False
        else:
            if tenta_riassegnazione(richiesta, assegnazioni, disponibilita, richieste, aule):
                motivazioni[richiesta.id] = "Assegnata dopo riassegnazione dinamica"
            else:
                assegnazioni[richiesta.id] = None
                motivazioni[richiesta.id] = "Impossibile assegnare: capienza insufficiente o slot occupati"

    return assegnazioni, motivazioni


def tenta_riassegnazione(richiesta_corrente, assegnazioni, disponibilita, richieste, aule):
    aule_candidate = [aula for aula in aule if aula.capienza >= richiesta_corrente.capienza_richiesta]

    for aula in aule_candidate:
        slot_bloccanti = [id_slot for id_slot in richiesta_corrente.slotIds
                          if not disponibilita[(aula.id_aula, richiesta_corrente.giorno, id_slot)]]

        if not slot_bloccanti:
            continue

        richieste_bloccanti = []
        for id_slot in slot_bloccanti:
            for r in richieste:
                if (assegnazioni.get(r.id) == aula.id_aula and r.giorno == richiesta_corrente.giorno
                        and id_slot in r.slotIds):
                    richieste_bloccanti.append(r)

        for richiesta_bloccante in richieste_bloccanti:
            nuova_aula = trova_nuova_aula(richiesta_bloccante, disponibilita, aule, preferenze=(
                richiesta_bloccante.prese, richiesta_bloccante.pc, richiesta_bloccante.proiettore))
            if nuova_aula:
                vecchia_aula = assegnazioni[richiesta_bloccante.id]
                assegnazioni[richiesta_bloccante.id] = nuova_aula.id_aula
                for id_slot in richiesta_bloccante.slotIds:
                    disponibilita[(vecchia_aula, richiesta_bloccante.giorno, id_slot)] = True
                    disponibilita[(nuova_aula.id_aula, richiesta_bloccante.giorno, id_slot)] = False

                assegnazioni[richiesta_corrente.id] = aula.id_aula
                for id_slot in richiesta_corrente.slotIds:
                    disponibilita[(aula.id_aula, richiesta_corrente.giorno, id_slot)] = False
                return True

    return False


def trova_nuova_aula(richiesta, disponibilita, aule, preferenze=None):
    prese_pref, pc_pref, proiettore_pref = preferenze if preferenze else (0, 0, 0)
    aule_ordinate = sorted(aule, key=lambda a: a.capienza)
    best_aula = None
    best_match = -1

    for aula in aule_ordinate:
        if aula.capienza >= richiesta.capienza_richiesta:
            if all(disponibilita[(aula.id_aula, richiesta.giorno, id_slot)] for id_slot in richiesta.slotIds):
                match = (
                    (prese_pref and aula.prese) +
                    (pc_pref and aula.pc) +
                    (proiettore_pref and aula.proiettore)
                )
                if match > best_match:
                    best_match = match
                    best_aula = aula

    return best_aula
