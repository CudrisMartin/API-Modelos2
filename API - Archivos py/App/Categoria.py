from flask import Flask, jsonify
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

    def __init_(self, id, nombre, puntaje):
        self.id = id
        self.nombre = nombre
        self.puntaje = puntaje

db.create_all()

#Esquema Videojuegos
class VideojuegoSchema(ma.Schema):
    class Meta:
        fields = ('nombre','puntaje')

#Unica respuesta
videojuego_schema = VideojuegoSchema()

#Multiple respuestas
videojuego_schema = VideojuegoSchema(many=True)

#GET
@app.route('/puntajes', methods = ['GET'])
def get_puntajes():
    todos_puntajes = Videojuego.query.all()
    result = videojuego_schema.dump(todos_puntajes)
    return jsonify(result)

#Mensaje Bienvenida
@app.route('/', methods = ['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido'})

#Ejecución de la app
if __name__ == '__main__':
    app.run(debug = True)