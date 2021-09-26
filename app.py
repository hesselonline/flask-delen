from som import Som, genereer_sommen
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.globals import session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
import os

SECRET_KEY = os.urandom(32)


class QuizForm(FlaskForm):

    naam = StringField("Wat is je naam?", validators=[DataRequired()])
    aantal = IntegerField("Hoeveel sommen wil je maken?",
                          validators=[DataRequired(),NumberRange(1,100)])
    submit = SubmitField("Beginnen")


class ExerciseForm(FlaskForm):
    antwoord = IntegerField("Wat is het antwoord?",
                            validators=[DataRequired()])
    rest = IntegerField("Wat is het rest getal?", validators=[Optional()])
    submit = SubmitField("Invoeren")


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def index():
    
    form = QuizForm()
    if form.validate_on_submit():
        session.clear()
        session["naam"] = form.naam.data
        session["aantal"] = form.aantal.data
        session["i"] = 0
        session["sommen"] = genereer_sommen(form.aantal.data)
        return redirect(url_for("exercise"))

    return render_template('index.html', form=form, aantal_goed = 0)


@app.route('/results')
def results():
    if "sommen" in session:
        sommen_goed = [ses for ses in session["sommen"] if ses["antwoord_correct"]]
        sommen_fout = [ses for ses in session["sommen"]
                    if ses["antwoord_correct"] == False and ses["antwoord"] != 0]
    else: 
        sommen_fout = []
        sommen_goed = []
    return render_template('results.html', sommen_goed=sommen_goed, sommen_fout=sommen_fout, aantal_goed = len(sommen_goed))


@app.route('/exercise', methods=["GET", "POST"])
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
        sommen[i]["antwoord_correct"] = form.antwoord.data == sommen[i]["resultaat"] and form.rest.data == sommen[i]["antwoord_rest"]

        if sommen[i]["antwoord_correct"]:
            flash(
                f'Inderdaad, het juiste antwoord was {sommen[i]["resultaat"]}, rest {sommen[i]["rest"]}!', "success")
        else:
            flash(f'Helaas, het juiste antwoord was {sommen[i]["resultaat"]}, rest {sommen[i]["rest"]}!',
                  "alert alert-danger alert-dismissible fade show")

        if session["aantal"] > session["i"]+1:
            session["i"] += 1
            return redirect(url_for("exercise"))

        else:
            return redirect(url_for("results"))

    return render_template('exercise.html', form=form, teller=sommen[i]["teller"], noemer=sommen[i]["noemer"], naam=naam, aantal=aantal, index=i+1, aantal_goed = len(sommen_goed))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)
