from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
from models import db, MsgFormIndex, Usuario

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'pg_index'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Você deve logar para acessar esta página.'


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

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
@login_required
def pg_dashboard():
    flash('Alerta! Aqui aparecerão os alertas da aplicação.', category='info')
    return render_template('dashboard.html')

@app.route('/desempenho-fisico')
@login_required
def pg_desempenho_fisico():
    flash('Clique sobre o jogador para mais detalhes dele na partida.', category='info')
    return render_template('desempenho-fisico.html')

@app.route('/desempenho-tecnico')
@login_required
def pg_desempenho_tecnico():
    flash('Clique sobre o gráfico para mais detalhes do jogador.', category='info')
    return render_template('desempenho-tecnico.html')

@app.route('/desempenho-tatico')
@login_required
def pg_desempenho_tatico():
    flash('Clique sobre o gráfico para mais detalhes do jogador.', category='info')
    return render_template('desempenho-tatico.html')

@app.route('/contato')
@login_required
def pg_contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('pg_index'))
    email = request.form['email']
    password = request.form['password']
    registered_user = Usuario.query.filter_by(email=email,password=password).first()
    if registered_user is None:
        flash('E-mail ou senha incorretos!' , 'danger')
        return redirect(url_for('pg_index'))
    login_user(registered_user, remember=(True if 'manterConectado' in request.form else False))
    next = request.args.get('next')

    return redirect(next or url_for('pg_dashboard'))

@app.route('/resetar-senha')
def esqueci_a_senha():
    pass

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pg_index'))

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
    port = int(os.environ.get("PORT", 8081))
    app.run(host='0.0.0.0', port=port, debug=True)
