from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])

class RegisForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
    name = StringField("name",validators=[DataRequired()])
    email = StringField("email", validators = [DataRequired()])

class ServiceForm(FlaskForm):
    date = DateField("date", validators = [DataRequired()])
    username = StringField("username", validators = [DataRequired()])
    content = SelectField("content", validators = [DataRequired()], 
    choices=[
        "",
        "Hidratação profunda", 
        "Cauterização", 
        "Reconstrução capilar", 
        "Escova progressiva sem formol",
        "Máscara capilar",
        "Alinhamento capilar"
    ])

