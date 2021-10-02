from utils.flash import flash_som_resultaat
from som import genereer_sommen, controleer_som
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.globals import session
from flask_bootstrap import Bootstrap
import os
import time
from utils.flash import flash_som_resultaat
from utils.forms import QuizForm, ExerciseForm

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        session.clear()
        session["naam"] = request.form.get("naam")
        return redirect(url_for("quiz"))

    return render_template("index.html", page="index", aantal_goed=0)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    form = QuizForm()
    if form.validate_on_submit():
        session["aantal"] = form.aantal.data
        session["i"] = 0
        session["avatar"] = None
        session["sommen"] = genereer_sommen(
            form.aantal.data, form.som_type.data, form.som_difficulty.data
        )
        session["start_tijd"] = time.time()
        session["eind_tijd"] = None
        return redirect(url_for("exercise"))

    return render_template(
        "quiz.html", page="quiz", naam=session["naam"], form=form, aantal_goed=0
    )


@app.route("/results")
def results():
    doorlooptijd = int((session["eind_tijd"] or time.time()) - session["start_tijd"])
    if "sommen" in session:
        sommen_goed = [ses for ses in session["sommen"] if ses["antwoord_correct"]]
        sommen_fout = [
            ses
            for ses in session["sommen"]
            if ses["antwoord_correct"] == False and ses["antwoord"] != 0
        ]
    else:
        sommen_fout = []
        sommen_goed = []
    return render_template(
        "results.html",
        page="results",
        naam=session["naam"],
        doorlooptijd=doorlooptijd,
        sommen_goed=sommen_goed,
        sommen_fout=sommen_fout,
        aantal_goed=len(sommen_goed),
    )


@app.route("/credits")
def credits():
    return render_template("credits.html", page="credits")


@app.route("/exercise", methods=["GET", "POST"])
def exercise():
    naam = session["naam"]
    percentage_style = str(int((session["i"] / session["aantal"]) * 100))
    aantal = session["aantal"]
    i = session["i"]
    sommen = session["sommen"]
    sommen_goed = [ses for ses in session["sommen"] if ses["antwoord_correct"]]

    form = ExerciseForm()
    if form.validate_on_submit():
        sommen[i]["antwoord"] = form.antwoord.data
        sommen[i]["antwoord_rest"] = form.rest.data
        sommen[i]["antwoord_correct"] = controleer_som(
            sommen[i], form.antwoord.data, form.rest.data
        )

        if sommen[i]["antwoord_correct"]:
            session["avatar"] = "happy"
        else:
            session["avatar"] = "angry"

        flash_som_resultaat(
            sommen[i]["antwoord_correct"],
            sommen[i]["resultaat"],
            sommen[i]["rest"],
            sommen[i]["type"],
        )

        if session["i"] + 1 < session["aantal"]:
            session["i"] += 1
            return redirect(url_for("exercise"))

        else:
            session["eind_tijd"] = time.time()
            return redirect(url_for("results"))

    return render_template(
        "exercise.html",
        page="exercise",
        form=form,
        som=sommen[i],
        naam=naam,
        aantal=aantal,
        percentage_style=percentage_style,
        index=i + 1,
        avatar=session["avatar"],
        aantal_goed=len(sommen_goed),
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
