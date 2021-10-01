from utils.flash import flash_som_resultaat
from som import genereer_sommen, controleer_som
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.globals import session
from flask_bootstrap import Bootstrap
import os
from utils.flash import flash_som_resultaat
from utils.forms import QuizForm, ExerciseForm

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def index():

    form = QuizForm()
    if form.validate_on_submit():
        session.clear()
        session["naam"] = form.naam.data
        session["aantal"] = form.aantal.data
        session["i"] = 0
        session["avatar"] = None
        session["sommen"] = genereer_sommen(
            form.aantal.data, form.som_type.data, form.som_difficulty.data
        )
        return redirect(url_for("exercise"))

    return render_template("index.html", form=form, aantal_goed=0)


@app.route("/results")
def results():
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
        naam=session["naam"],
        sommen_goed=sommen_goed,
        sommen_fout=sommen_fout,
        aantal_goed=len(sommen_goed),
    )

@app.route("/credits")
def credits():
    return render_template(
        "credits.html"
    )


@app.route("/exercise", methods=["GET", "POST"])
def exercise():
    naam = session["naam"]
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

        if  session["i"] +1 < session["aantal"]:
            session["i"] += 1
            return redirect(url_for("exercise"))

        else:
            return redirect(url_for("results"))

    return render_template(
        "exercise.html",
        form=form,
        som=sommen[i],
        naam=naam,
        aantal=aantal,
        index=i + 1,
        avatar = session["avatar"],
        aantal_goed=len(sommen_goed),
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
