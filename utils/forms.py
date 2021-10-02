from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField,SelectField
from wtforms.validators import DataRequired, Optional, NumberRange

class QuizForm(FlaskForm):

    aantal = IntegerField("Hoeveel sommen wil je maken?",
                          validators=[DataRequired(), NumberRange(1, 100)], render_kw={'autofocus': True})
    som_type = SelectField('Soort oefeningen', choices=[
                          ('d', 'Delen'), ('m', 'Vermenigvuldigen'), ('s_a','Optellen en aftrekken')])
    som_difficulty = SelectField('Soort oefeningen', choices=[
                          ('1', 'Makkelijk'), ('2', 'Gemiddeld'), ('3', 'Moeilijk')])
    submit = SubmitField("Beginnen")

class ExerciseForm(FlaskForm):
    antwoord = IntegerField("Wat is het antwoord?",
                            validators=[DataRequired()])
    rest = IntegerField("Wat is het rest getal?", validators=[Optional()])
    submit = SubmitField("Controleer")