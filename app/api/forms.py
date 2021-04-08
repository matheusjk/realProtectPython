from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import DateTimeField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, URL, Email, ValidationError, EqualTo, Regexp
from datetime import datetime

class ApiForm(FlaskForm):
    dataInicio = DateTimeLocalField("Data Inicio", default=datetime.today, format="%d/%m/%Y %H:%M:%S", validators=[DataRequired(message="Voce precisa inserir a data inicio")])
    dataFim = DateTimeLocalField("Data Fim", default=datetime.today, format="%d/%m/%Y %H:%M:%S", validators=[DataRequired(message="Voce presica inserir uma data final")])
    contenha = StringField("Contenha") 
    submit = SubmitField("Buscar")

    def validate_on_submit(self):
        resultado = super(ApiForm, self).validate()
        print("DATA INICIO {} | DATA FIM {}".format(self.dataInicio.data, self.dataFim.data))
        if self.dataInicio.data > self.dataFim.data:
            return False
        else:
            return resultado
