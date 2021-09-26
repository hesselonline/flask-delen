from math import floor
import random


class Som():
    def __init__(self, teller, noemer):
        self.teller = teller
        self.noemer = noemer
        self.resultaat = int(floor(self.teller/self.noemer))
        self.rest = int(self.teller % self.noemer)
        self.antwoord = 0
        self.antwoord_rest = 0
        self.antwoord_correct = False
    
    
def genereer_sommen(aantal):

    som_lijst =[]
    i = 0

    while i < aantal:
        som = Som(random.randint(1000, 10000),random.randint(10, 100)).__dict__
        som_lijst.append(som)

        i += 1

    return som_lijst


