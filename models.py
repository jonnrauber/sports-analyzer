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

class Clube(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    telefone = db.Column(db.String(20), nullable = False)
    usuarios = db.relationship('Usuario', backref='clube', lazy=False)

    def __repr__(self):
        return '<Clube %r>' % self.nome

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
