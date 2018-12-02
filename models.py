# apps.members.models
import flask_login
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MsgFormIndex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    clube = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<MsgFormIndex %r>' % self.nome

class Clube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    jogos = db.relationship("Jogo", foreign_keys="Jogo.id_time", backref="clube", lazy="dynamic")

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password = db.Column(db.String(200))
    nome = db.Column(db.String(), nullable=False)
    data_de_registro = db.Column(db.DateTime)
    id_clube = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    clube = db.relationship('Clube')

    def __init__(self, email, password, id_clube, nome):
        self.email = email
        self.password = password
        self.nome = nome
        self.id_clube = id_clube
        self.data_de_registro = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class EsquemaTatico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formacao = db.Column(db.String(10), nullable=False)

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.Integer, nullable=False) #1 para mandante e 0 para visitante
    id_time = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    time = db.relationship('Clube', foreign_keys=[id_time])
    id_adversario = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    adversario = db.relationship('Clube', foreign_keys=[id_adversario])
    id_esquema_tatico = db.Column(db.Integer, db.ForeignKey('esquema_tatico.id'), nullable=False)
    esquema_tatico = db.relationship('EsquemaTatico')

class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

class Modulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)

class TipoEstatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    id_modulo = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    modulo = db.relationship('Modulo', foreign_keys=[id_modulo])

class Estatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_jogo = db.Column(db.Integer, db.ForeignKey('jogo.id'), nullable=False)
    jogo = db.relationship('Jogo', foreign_keys=[id_jogo])
    id_jogador = db.Column(db.Integer, db.ForeignKey('jogador.id'), nullable=False)
    jogador = db.relationship('Jogador', foreign_keys=[id_jogador])
    id_estatistica = db.Column(db.Integer, db.ForeignKey('tipo_estatistica.id'), nullable=False)
    estatistica = db.relationship('TipoEstatistica', foreign_keys=[id_estatistica])
    quantidade = db.Column(db.Integer, nullable=False)