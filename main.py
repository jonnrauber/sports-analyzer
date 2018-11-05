from flask import Flask, render_template, request, redirect, flash, send_from_directory
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo=nome_arquivo)

@app.route('/')
def pg_index():
    return render_template('index.html')

@app.route('/desempenho-fisico')
def pg_desempenho_fisico():
    pass

@app.route('/desempenho-tecnico')
def pg_desempenho_tecnico():
    pass

@app.route('/desempenho-tatico')
def pg_desempenho_tatico():
    pass

@app.route('/contato')
def pg_contato():
    pass


app.run(host='0.0.0.0', port=8081, debug=True)
