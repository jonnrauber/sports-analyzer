from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MsgFormIndex(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    telefone = db.Column(db.String(20), nullable = False)
    clube = db.Column(db.String(40), nullable = False)

    def __repr__(self):
        return '<MsgFormIndex %r>' % self.nome

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    senha = db.Column(db.String(256), nullable = False)
    telefone = db.Column(db.String(20), nullable = False)
    clube_id = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    msgs_form_contato = db.relationship('MsgFormContato', backref='usuario', lazy=False)

    def __repr__(self):
        return '<Usuario %r>' % self.email

class MsgFormContato(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    assunto = db.Column(db.Text, nullable = False)
    mensagem = db.Column(db.Text, nullable = False)
    data = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<MsgFormContato %r>' % self.id

class Clube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    jogos = db.relationship("Jogo", backref="clube", lazy="dynamic")

class EsquemaTatico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formacao = db.Column(db.String(10), nullable=False)

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.Integer, nullable=False) #1 para mandante e 0 para visitante
    id_time = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    time = db.relationship('Clube')
    id_adversario = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    adversario = db.relationship('Clube')
    id_esquema_tatico = db.Column(db.Integer, db.ForeignKey('esquema_tatico.id'), nullable=False)
    esquema_tatico = db.relationship('EsquemaTatico')

class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

class TipoEstatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

class Estatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_jogo = db.Column(db.Integer, db.ForeignKey('jogo.id'), nullable=False)
    jogo = db.relationship('Jogo')
    id_jogador = db.Column(db.Integer, db.ForeignKey('jogador.id'), nullable=False)
    jogador = db.relationship('Jogador')
    id_estatistica = db.Column(db.Integer, db.ForeignKey('tipo_estatistica.id'), nullable=False)
    estatistica = db.relationship('Estatistica')
    quantidade = db.Column(db.Integer, nullable=False)
