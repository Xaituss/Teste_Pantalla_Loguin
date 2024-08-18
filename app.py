from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

'''
Esta función manda los datos del usuario a la API para registrarlo.
'''
def registrar_usuario(username, password):
    url = "https://tu-api.com/registrar"  # La URL de la API de registro
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    return response.status_code == 200  # Si todo salió bien, devuelve True

'''
Función para hacer login: manda el username y password a la API.
'''
def hacer_login(username, password):
    url = "https://tu-api.com/login"  # La URL de la API de login
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("token")  # Si el login fue exitoso, devuelve el token
    return None  # Si no, devuelve None

'''
Ruta para la página de login. Maneja GET y POST.
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ""  # Mensaje de error vacío al inicio
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = hacer_login(username, password)
        if token:
            return redirect(url_for('success', token=token))  # Si el login fue bien, redirige a la página de éxito
        else:
            error_message = "Credenciales incorrectas"  # Si no, muestra este error
    return render_template('login.html', error_message=error_message)

'''
Ruta para la página de registro. Similar a la de login.
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = ""  # Igual, empezamos sin mensaje de error
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if registrar_usuario(username, password):
            token = hacer_login(username, password)
            if token:
                return redirect(url_for('success', token=token))  # Si todo salió bien, redirige a la página de éxito
            else:
                error_message = "Error al registrar, intenta de nuevo"  # Algo salió mal después del registro
        else:
            error_message = "Error al registrar, intenta de nuevo"  # Algo salió mal con el registro
    return render_template('register.html', error_message=error_message)

'''
Ruta que se muestra si el login es exitoso.
'''
@app.route('/success')
def success():
    token = request.args.get('token')  # Obtenemos el token de la URL
    return render_template('success.html', token=token)  # Mostramos el token en la página

'''
Arrancamos la app con Flask.
'''
if __name__ == '__main__':
    app.run(debug=True)
