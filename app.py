import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
import secrets

app = Flask(__name__)

# Generar y asignar una clave secreta aleatoria si no está definida en las variables de entorno
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_urlsafe(16))

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# Verificación de configuración (solo para depuración, eliminar en producción)
print("MAIL_USERNAME:", app.config['MAIL_USERNAME'])
print("MAIL_PASSWORD:", app.config['MAIL_PASSWORD'])

# Rutas de la aplicación
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/vision-mision')
def vision_mision():
    return render_template('vision_mision.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Ruta para enviar el mensaje desde el formulario de contacto
@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Validar los datos del formulario
    if not name or not email or not message:
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('contacto'))

    # Crear el mensaje de correo
    msg = Message(
        subject=f'Mensaje de Contacto de {name}',
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']]
    )
    msg.body = f'Nombre: {name}\nCorreo Electrónico: {email}\n\nMensaje:\n{message}'

    try:
        msg = Message(
            subject=f'Mensaje de Contacto de {name}',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = f'Nombre: {name}\nCorreo Electrónico: {email}\n\nMensaje:\n{message}'
        mail.send(msg)
        flash('Mensaje enviado correctamente', 'success')
        print('Correo enviado exitosamente')
    except Exception as e:
        flash('Error al enviar el mensaje. Por favor, intenta nuevamente.', 'danger')
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")
        print(f"Error args: {e.args}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
