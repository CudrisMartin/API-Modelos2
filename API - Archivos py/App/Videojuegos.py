from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:usuario@localhost:3306/videojuegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


ma = Marshmallow(app)

#Creación tablas
class Videojuego(db.Model):
    
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(255))
    puntaje = db.Column(db.Integer)

    def __init__(self, nombre, puntaje):
        self.nombre = nombre
        self.puntaje = puntaje

db.create_all()

#Esquema Videojuegos
class VideojuegoSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','puntaje')

#Unica respuesta
videojuego_schema = VideojuegoSchema()

#Multiple respuestas
videojuegos_schema = VideojuegoSchema(many=True)

#GET
@app.route('/puntajes', methods = ['GET'])
def get_puntajes():
    todos_puntajes = Videojuego.query.all()
    result = videojuegos_schema.dump(todos_puntajes)
    return jsonify(result)

#GET elemento segun id
@app.route('/puntajes/<id>', methods = ['GET'])
def get_puntaje_id(id):
    puntaje = Videojuego.query.get(int(id))
    return videojuego_schema.jsonify(puntaje)

#POST
@app.route('/puntajes', methods = ['POST'])
def ingresar_puntaje():
    data = request.get_json(force = True)
    nombre = data['nombre']
    puntaje = data['puntaje']

    nuevo_puntaje = Videojuego(nombre, puntaje)

    db.session.add(nuevo_puntaje)
    db.session.commit()
    
    return videojuego_schema.jsonify(nuevo_puntaje) 

#Mensaje Bienvenida
@app.route('/', methods = ['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido'})

#Ejecución de la app
if __name__ == '__main__':
    app.run(debug = True)