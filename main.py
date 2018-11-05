from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo=nome_arquivo)

@app.route('/')
def pg_index():
    return render_template('index.html')

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

app.run(host='0.0.0.0', port=8081, debug=True)
