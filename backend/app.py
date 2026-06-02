from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Permite que React se conecte a la API sin bloqueos de seguridad

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    """Inicializa la base de datos y crea un usuario administrador por defecto"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # SE CORRIGIÓ: NOT NULL en lugar de NOT EXISTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insertar usuario admin por defecto si la tabla está vacía
    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (username, password) VALUES ('admin', 'admin123')")
    
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar el servidor
init_db()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username_ingresado = data.get('username')
    password_ingresado = data.get('password')

    if not username_ingresado or not password_ingresado:
        return jsonify({"success": False, "message": "Datos incompletos."}), 400

    # Buscar las credenciales directamente en SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username_ingresado, password_ingresado))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({"success": True, "message": f"Bienvenido, {username_ingresado}"})
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos."}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)