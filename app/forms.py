from wtforms import SubmitField, StringField, PasswordField, Form, IntegerField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class ContestForm(Form):
    problem1 = IntegerField('Problem 1', validators=[DataRequired()])
    problem2 = IntegerField('Problem 2', validators=[DataRequired()])
    problem3 = IntegerField('Problem 3', validators=[DataRequired()])
    problem4 = IntegerField('Problem 4', validators=[DataRequired()])