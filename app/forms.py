from wtforms import SubmitField, StringField, PasswordField, Form, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class CreateContestForm(Form):
    contest_name = StringField('Contest Name', validators=[DataRequired()])
    answer_fields = FieldList(FormField(StringField('Answer', validators=[DataRequired()])), min_entries=30, max_entries=30)