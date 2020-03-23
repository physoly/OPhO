from wtforms import SubmitField, StringField, PasswordField, Form
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])