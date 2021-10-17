from math import floor
import random


class Som:
    def __init__(self, i, teller, noemer, som_type="d", som_difficulty="3"):
        """Create new instance of sum and calculate answer."""

        tekst_translate = {"d": "÷", "s": "-", "a": "+", "m": "x", "dd": "÷"}

        self.teller = teller
        self.noemer = noemer
        self.antwoord = None
        self.antwoord_rest = 0
        self.antwoord_correct = None
        self.type = som_type
        self.difficulty = som_difficulty
        self.tekst = tekst_translate[som_type]
        self.resultaat = bereken_resultaat(teller, noemer, som_type)
        self.rest = bereken_rest(teller, noemer, som_type)
        self.id = i


def bereken_resultaat(teller, noemer, som_type):
    if som_type == "d":
        return int(floor(teller / noemer))
    if som_type == "dd":
        return teller / noemer
    if som_type == "s":
        return int(teller - noemer)
    if som_type == "a":
        return int(teller + noemer)
    if som_type == "m":
        return int(teller * noemer)


def bereken_rest(teller, noemer, som_type):
    if som_type == "d":
        return int(teller % noemer)


def genereer_sommen(aantal, som_type, som_difficulty):

    som_lijst = []
    i = 0

    difficulty_translate = {
        "d": {
            "1": {"teller": {"min": 10, "max": 100}, "noemer": {"min": 1, "max": 10}},
            "2": {
                "teller": {"min": 100, "max": 1000},
                "noemer": {"min": 10, "max": 100},
            },
            "3": {
                "teller": {"min": 1000, "max": 10000},
                "noemer": {"min": 10, "max": 100},
            },
        },
        "dd": {
            "1": {"teller": {"min": 0.0, "max": 20.0}, "noemer": {"min": 1.0, "max": 10.0}},
            "2": {
                "teller": {"min": 0.0, "max": 20.0},
                "noemer": {"min": 1.0, "max": 100.0},
            },
            "3": {
                "teller": {"min": 0.0, "max": 50.0},
                "noemer": {"min": 1.0, "max": 1000.0},
            },
        },
        "m": {
            "1": {"teller": {"min": 1, "max": 10}, "noemer": {"min": 1, "max": 5}},
            "2": {"teller": {"min": 1, "max": 10}, "noemer": {"min": 1, "max": 12}},
            "3": {"teller": {"min": 1, "max": 10}, "noemer": {"min": 1, "max": 20}},
        },
        "s": {
            "1": {"teller": {"min": 1, "max": 10}, "noemer": {"min": 1, "max": 10}},
            "2": {
                "teller": {"min": 10, "max": 100},
                "noemer": {"min": 10, "max": 100},
            },
            "3": {
                "teller": {"min": 100, "max": 1000},
                "noemer": {"min": 100, "max": 1000},
            },
        },
        "a": {
            "1": {"teller": {"min": 1, "max": 10}, "noemer": {"min": 1, "max": 10}},
            "2": {
                "teller": {"min": 10, "max": 100},
                "noemer": {"min": 10, "max": 100},
            },
            "3": {
                "teller": {"min": 100, "max": 1000},
                "noemer": {"min": 100, "max": 1000},
            },
        },
    }

    while i < aantal:

        def som_type_rand(som_type):
            if som_type == "s_a":
                return random.choice(["s", "a"])
            else:
                return som_type

        if som_type == "dd":

            noemer = round(
                random.uniform(
                    difficulty_translate[som_type_rand(som_type)][som_difficulty][
                        "noemer"
                    ]["min"],
                    difficulty_translate[som_type_rand(som_type)][som_difficulty][
                        "noemer"
                    ]["max"],
                ),
                2,
            )
            teller = (
                round(
                    (
                        random.uniform(
                            difficulty_translate[som_type_rand(som_type)][
                                som_difficulty
                            ]["teller"]["min"],
                            difficulty_translate[som_type_rand(som_type)][
                                som_difficulty
                            ]["teller"]["max"],
                        )
                    ),
                    2,
                )
                * noemer
            )

        else:

            teller = random.randint(
                difficulty_translate[som_type_rand(som_type)][som_difficulty]["teller"][
                    "min"
                ],
                difficulty_translate[som_type_rand(som_type)][som_difficulty]["teller"][
                    "max"
                ],
            )
            noemer = random.randint(
                difficulty_translate[som_type_rand(som_type)][som_difficulty]["noemer"][
                    "min"
                ],
                min(
                    teller,
                    difficulty_translate[som_type_rand(som_type)][som_difficulty][
                        "noemer"
                    ]["max"],
                ),
            )

        som = Som(
            i,
            teller,
            noemer,
            som_type_rand(som_type),
        ).__dict__
        

        if teller == round(teller, 4):
            som_lijst.append(som)
            i += 1

    return som_lijst


def controleer_som(som: dict, antwoord: int, antwoord_rest: int = None):
    return som["resultaat"] == antwoord and (
        (
            (antwoord_rest == None or antwoord_rest == 0)
            and (som["rest"] == 0 or som["rest"] == None)
        )
        or antwoord_rest == som["rest"]
    )
