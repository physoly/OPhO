from wtforms import SubmitField, StringField, PasswordField, Form, IntegerField, FieldList
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class ContestForm(Form):
    problems = FieldList(IntegerField(validators=[DataRequired()]), min_entries=30, max_entries=30)