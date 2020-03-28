from wtforms import SubmitField, StringField, PasswordField, Form, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class ProblemForm(Form):
    answer = IntegerField('Answer', validators=[])
class ContestForm(Form):
    problems = FieldList(FormField(ProblemForm), min_entries=30, max_entries=30)