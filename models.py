# apps.members.models
import flask_login
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Chart():
    def __init__(self, labels, values, colors, tipo_estatistica):
        self.labels = labels
        self.values = values
        self.colors = colors
        self.tipo_estatistica = tipo_estatistica

class MsgFormIndex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    clube = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<MsgFormIndex %r>' % self.nome

class MsgContato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario')
    assunto = db.Column(db.String(50), nullable=False)
    mensagem = db.Column(db.String(500), nullable=False)
    data = db.Column(db.DateTime)

    def __init__(self, id_usuario, assunto, mensagem):
        self.id_usuario = id_usuario
        self.assunto = assunto
        self.mensagem = mensagem
        self.data = datetime.now()

class Clube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    jogos = db.relationship("Jogo", foreign_keys="Jogo.id_time", backref="clube", lazy="dynamic")
    jogadores = db.relationship("Jogador", foreign_keys="Jogador.id_clube", lazy="dynamic")

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password = db.Column(db.String(200))
    nome = db.Column(db.String(), nullable=False)
    data_de_registro = db.Column(db.DateTime)
    id_clube = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    clube = db.relationship('Clube')
    id_role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role')

    def __init__(self, email, password, id_clube, nome, id_role):
        self.email = email
        self.password = password
        self.nome = nome
        self.id_clube = id_clube
        self.data_de_registro = datetime.utcnow()
        self.id_role = id_role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_role(self):
        return self.role

class EsquemaTatico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formacao = db.Column(db.String(10), unique=True, nullable=False)

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
    placar_time = db.Column(db.Integer, nullable=False)
    placar_adversario = db.Column(db.Integer, nullable=False)

    def __init__(self, data, local, id_time, id_adversario, id_esquema_tatico, placar_time, placar_adversario):
        self.data = data
        self.local = local
        self.id_time = id_time
        self.id_adversario = id_adversario
        self.id_esquema_tatico = id_esquema_tatico
        self.placar_time = placar_time
        self.placar_adversario = placar_adversario

class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    id_clube = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    clube = db.relationship('Clube')
    altura = db.Column(db.Integer) #em cm
    peso = db.Column(db.Integer) #em kg

    def __init__(self, nome, idade, id_clube, altura=None, peso=None):
        self.nome = nome
        self.idade = idade
        self.id_clube = id_clube
        self.altura = altura
        self.peso = peso

class Modulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)

class TipoEstatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    id_modulo = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    modulo = db.relationship('Modulo', foreign_keys=[id_modulo])
    unidade_medida = db.Column(db.String(10))

    def __init__(self, nome, id_modulo, unidade_medida=''):
        self.nome = nome
        self.id_modulo = id_modulo
        self.unidade_medida = unidade_medida

class Estatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_jogo = db.Column(db.Integer, db.ForeignKey('jogo.id'), nullable=False)
    jogo = db.relationship('Jogo', foreign_keys=[id_jogo])
    id_jogador = db.Column(db.Integer, db.ForeignKey('jogador.id'), nullable=False)
    jogador = db.relationship('Jogador', foreign_keys=[id_jogador])
    id_tipo_estatistica = db.Column(db.Integer, db.ForeignKey('tipo_estatistica.id'), nullable=False)
    tipo_estatistica = db.relationship('TipoEstatistica', foreign_keys=[id_tipo_estatistica])
    quantidade = db.Column(db.Integer, nullable=False)

    def __init__(self, id_jogo, id_jogador, id_tipo_estatistica, quantidade):
        self.id_jogo = id_jogo
        self.id_jogador = id_jogador
        self.id_tipo_estatistica = id_tipo_estatistica
        self.quantidade = quantidade
