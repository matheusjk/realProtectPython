from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField, EmailField, IntegerField, TelField, DateField
from wtforms.validators import DataRequired, Length, URL, EqualTo, Email, ValidationError


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[Email(message="Não é um email valido"), DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    submit = SubmitField('Efetuar Login')


class CadastroUsuario(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = EmailField("email", validators=[Email(message="Não é um email valido"), DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    botaoVolta = SubmitField("Voltar")
    submit = SubmitField("Enviar")


class Usuario(FlaskForm):
    # id = IntegerField("id")
    nome = StringField('Nome', validators=[DataRequired()])
    email = EmailField("Email", validators=[Email(message="Não é um email valido"), DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmarSenha = PasswordField('Repete Senha', validators=[DataRequired(message="Por favor insira a senha"),
                                                               EqualTo("senha", message="Senhas devem ser iguais"),
                                                               Length(min=5, max=30,
                                                                      message="Senha deve ter no minimo 5 caracteres")])
    submit = SubmitField('Enviar')


class Recuperar(FlaskForm):
    email = EmailField("email", validators=[Email(message="Não é um email valido"), DataRequired()])
    submit = SubmitField("Enviar")