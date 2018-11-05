from flask import Flask, render_template, request, redirect, flash, send_from_directory
import os

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
