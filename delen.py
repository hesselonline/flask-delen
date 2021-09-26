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
    
    def geef_antwoord(self, antwoord, antwoord_rest):
        self.antwoord = antwoord
        self.antwoord_rest = antwoord_rest

        if self.antwoord == self.resultaat and self.antwoord_rest == self.rest:

            self.antwoord_correct = True

        else:

            self.antwoord_correct = False

    def rapport(self):
        if self.antwoord_correct:
            print("Je had deze som goed!!")
        else:
            print("De volgende som ging bij jou fout: ")
            print(f"De som was {self.teller} gedeeld door {self.noemer}, het goede antwoord is {self.resultaat} rest {self.rest}. Jij gaf als antwoord {self.antwoord} rest {self.antwoord_rest}. ")





naam = input("Wat is je naam? ")
print(f"Hallo, {naam}!")
som_lijst = []

aantal = int(input("Hoeveel sommen wil je oefenen? "))
i = 0

while i < aantal:
    som = Som(random.randint(1000, 10000),random.randint(10, 100))
    som_lijst.append(som)

    i += 1


for som in som_lijst:

    print(f"Wat is {som.teller} gedeeld door {som.noemer}?")
    antwoordInput = input("Geef het antwoord als volgt: XXX rest YY! ")

    try:
        antwoorden = antwoordInput.split("rest")
        antwoord = int(antwoorden[0].strip())
    except:
        antwoordInput = input("Geef het antwoord als volgt: XXX rest YY! ")
        antwoorden = antwoordInput.split("rest")
        antwoord = int(antwoorden[0].strip())

    try:
        antwoord_rest = int(antwoorden[1].strip())
    except IndexError:
        antwoord_rest = 0

    if som.geef_antwoord(antwoord, antwoord_rest):
        
        print("Dat is goed!!!")
    else:
        print(f"Helaas, het goede antwoord is {som.resultaat}, rest {som.rest}")

    print("------------------------------------------------")


antwoorden_goed = [x for x in som_lijst if x.antwoord_correct]
antwoorden_fout = [x for x in som_lijst if not x.antwoord_correct]
print(
    f"Je hebt {len(antwoorden_goed)} antwoorden goed en {len(antwoorden_fout)} antwoorden fout!")

for som in antwoorden_fout:
    som.rapport()

    

