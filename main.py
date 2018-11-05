from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class MsgFormIndex(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    telefone = db.Column(db.String(20), nullable = False)
    clube = db.Column(db.String(40), nullable = False)

    def __repr__(self):
        return '<MsgFormIndex %r>' % self.nome

def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo=nome_arquivo)

@app.route('/', methods=['GET'])
def pg_index():
    return render_template('index.html')

@app.route('/ebook-sports-analyzer.pdf')
def download_ebook():
    return send_from_directory('static', 'ebook-sports-analyzer.pdf')

@app.route('/', methods=['POST'])
def contato_index():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    clube = request.form.get('clube')
    msg = MsgFormIndex(nome=nome, email=email, telefone=telefone, clube=clube)
    db.session.add(msg)
    db.session.commit()
    flash('Mensagem enviada com sucesso!', category='success')
    return redirect(url_for('pg_index'))


@app.route('/dashboard')
def pg_dashboard():
    return render_template('dashboard.html')

@app.route('/desempenho-fisico')
def pg_desempenho_fisico():
    return render_template('desempenho-fisico.html')

@app.route('/desempenho-tecnico')
def pg_desempenho_tecnico():
    return render_template('desempenho-tecnico.html')

@app.route('/desempenho-tatico')
def pg_desempenho_tatico():
    return render_template('desempenho-tatico.html')

@app.route('/contato')
def pg_contato():
    return render_template('contato.html')

@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('pg_dashboard'))

@app.route('/resetar-senha')
def esqueci_a_senha():
    pass

@app.route('/logout')
def logout():
    return redirect(url_for('pg_index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
