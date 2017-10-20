#!/usr/local/bin/python3

import argparse
import random

membri = (('Ana',),
          ('Enrique', 'Concha'),
          ('Ester',),
          ('Federico', 'Teresa'),
          ('Giancarlo',),
          ('Giuseppe', 'Noemi'),
          ('Isabel',),
          ('Juanita',),
          ('Marcelo', 'Chantal'),
          ('Maria',),
          ('Marta',),
          ('Michele', 'Federica'),
          ('Philippe',),
          ('Tommaso', 'Laura')
          )

#TODO parse arguments to remove names
da_rimuovere = (('Ana',),)

#TODO parse arguments define group size
persone_per_gruppo = 5

def copia_lista(membri):
    membri_l = [(x, len(x)) for x in membri]
    return(membri_l)

def rimuovi_membri(membri_l, da_rimuovere):
    for nome in da_rimuovere:
        membri_l.remove((nome, len(nome)))
    return membri_l

def genera_gruppi(membri, persone_per_gruppo, da_rimuovere = None):
    membri = copia_lista(membri)
    membri = rimuovi_membri(membri, da_rimuovere)
    gruppi = []
    while len(membri) > 0:
        gruppo, persone = [], 0
        while persone < persone_per_gruppo and len(membri) > 0:
            membro = membri.pop(random.randrange(len(membri)))
            persone += membro[1]
            gruppo.append(membro[0])
        gruppi.append(gruppo)
    return gruppi

def formatta_gruppi(membri, persone_per_gruppo, da_rimuovere):
    gruppi = genera_gruppi(membri, persone_per_gruppo, da_rimuovere)
    for i, gruppo in enumerate(gruppi, start=1):
        print('Gruppo', i, end=': ')
        componenti = len(gruppo)
        for i, membro in enumerate(gruppo, start=1):
            num_pers = len(membro)
            if num_pers == 1:
                print(membro[0], end='')
            elif num_pers == 2:
                print(membro[0], '&', membro[1], end='')
            else:
                raise ValueError('Sono supportati solo singoli membri o coppie.')
            if i < componenti: print(', ', end='')
        print('')
    return None

def main(): formatta_gruppi(membri, persone_per_gruppo, da_rimuovere)

if __name__ == '__main__': main()
