from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/prueba_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Ruta principal para mostrar el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Agregar cliente
@app.route('/clientes', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    nuevo_cliente = Cliente(nombre=nombre, email=email)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return redirect('/')

# Actualizar cliente
@app.route('/clientes/actualizar', methods=['POST'])
def actualizar_cliente():
    cliente_id = request.form['id']
    nombre = request.form['nombre']
    email = request.form['email']
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        cliente.nombre = nombre
        cliente.email = email
        db.session.commit()
    return redirect('/')

# Eliminar cliente
@app.route('/clientes/eliminar', methods=['POST'])
def eliminar_cliente():
    cliente_id = request.form['id']
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
    return redirect('/')

# Ver clientes
@app.route('/clientes/ver', methods=['GET'])
def ver_clientes():
    clientes = Cliente.query.all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'email': c.email} for c in clientes])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
