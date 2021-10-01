from flask import flash


def flash_som_resultaat(som_correct: bool, som_resultaat: int, som_rest: int, som_type: str):

    if som_correct and som_type != "d":
        flash(
            f'Inderdaad, het juiste antwoord was {som_resultaat}!', "success")
    if som_correct and som_type == "d":
        flash(
            f'Inderdaad, het juiste antwoord was {som_resultaat}, rest {som_rest}!', "success")
    if som_correct == False and som_type != "d":
        flash(f'Helaas, het juiste antwoord was {som_resultaat}!',
                     "alert alert-danger alert-dismissible fade show")
    if som_correct == False and som_type == "d":
        flash(f'Helaas, het juiste antwoord was {som_resultaat}, rest {som_rest}!',
                     "alert alert-danger alert-dismissible fade show")
