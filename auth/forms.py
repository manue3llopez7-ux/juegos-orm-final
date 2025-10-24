# auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# ✅ Asegúrate de importar 'Length' aquí
from wtforms.validators import DataRequired, EqualTo, Length 

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')

class RegistrationForm(FlaskForm):
    # Ahora la validación Length funcionará
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8), EqualTo('confirm_password', message='Las contraseñas deben coincidir')])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar')
    
    # Validación personalizada para unicidad (username/email)
    def validate_username(self, username):
        # Asegúrate de que esta importación esté dentro de la función o que el controlador exista
        from controlador_usuarios import obtener_usuario_por_username 
        if obtener_usuario_por_username(username.data):
            from wtforms import ValidationError
            raise ValidationError('Ese nombre de usuario ya está en uso.')