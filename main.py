from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
from models import db, MsgFormIndex, MsgContato, Usuario, TipoEstatistica, Estatistica, Jogador, Jogo, Chart
import random

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

def chartEstatisticas(estatisticas):
    labels = []
    values = []
    colors = []
    for e in estatisticas:
        labels.append(e.jogador.nome)
        values.append(e.quantidade)
        c = lambda: random.randint(0,255)
        colors.append('#%02X%02X%02X' % (c(), c(), c()))
    return Chart(labels, values, colors)

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
    return render_template('dashboard.html')

@app.route('/desempenho-fisico', methods=["GET", "POST"])
@login_required
def pg_desempenho_fisico():
    tipos_estatistica = TipoEstatistica.query.filter_by(id_modulo=1)
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    estatisticas = []
    id_tipo_estatistica = None
    id_jogo = None
    if request.method == 'POST':
        id_jogo = request.form['id_jogo']
        id_tipo_estatistica = request.form['id_tipo_estatistica']

        if id_tipo_estatistica != None:
            estatisticas = Estatistica.query \
                                    .filter_by(id_tipo_estatistica=id_tipo_estatistica) \
                                    .join(Jogo) \
                                    .filter_by(id_time=current_user.id_clube, id=id_jogo) \
                                    .all()
        flash('Clique sobre o jogador para mais detalhes.', category='info')
    else:
        id_tipo_estatistica = request.args.get('id_tipo_estatistica')
    return render_template('desempenho-fisico.html', tipos_estatistica=tipos_estatistica, id_jogo=id_jogo, \
                            estatisticas=estatisticas, jogos=jogos, id_tipo_estatistica=id_tipo_estatistica)

@app.route('/desempenho-tecnico', methods=['GET', 'POST'])
@login_required
def pg_desempenho_tecnico():
    tipos_estatistica = TipoEstatistica.query.filter_by(id_modulo=2)
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    estatisticas = []
    id_tipo_estatistica = None
    id_jogo = None
    chart = []
    if request.method == 'POST':
        id_jogo = request.form['id_jogo']
        id_tipo_estatistica = request.form['id_tipo_estatistica']

        if id_tipo_estatistica != None:
            estatisticas = Estatistica.query \
                                    .filter_by(id_tipo_estatistica=id_tipo_estatistica) \
                                    .join(Jogo) \
                                    .filter_by(id_time=current_user.id_clube, id=id_jogo) \
                                    .all()

            chart = chartEstatisticas(estatisticas)
        flash('Clique sobre o jogador para mais detalhes.', category='info')
    else:
        id_tipo_estatistica = request.args.get('id_tipo_estatistica')
    return render_template('desempenho-tecnico.html', tipos_estatistica=tipos_estatistica, id_jogo=id_jogo, \
                            estatisticas=estatisticas, jogos=jogos, id_tipo_estatistica=id_tipo_estatistica, \
                            chart=chart)

@app.route('/desempenho-tatico', methods=['GET', 'POST'])
@login_required
def pg_desempenho_tatico():
    tipos_estatistica = TipoEstatistica.query.filter_by(id_modulo=3)
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    estatisticas = []
    id_tipo_estatistica = None
    id_jogo = None
    if request.method == 'POST':
        id_jogo = request.form['id_jogo']
        id_tipo_estatistica = request.form['id_tipo_estatistica']

        if id_tipo_estatistica != None:
            estatisticas = Estatistica.query \
                                    .filter_by(id_tipo_estatistica=id_tipo_estatistica) \
                                    .join(Jogo) \
                                    .filter_by(id_time=current_user.id_clube, id=id_jogo) \
                                    .all()
        flash('Clique sobre o jogador para mais detalhes.', category='info')
    else:
        id_tipo_estatistica = request.args.get('id_tipo_estatistica')
    return render_template('desempenho-tatico.html', tipos_estatistica=tipos_estatistica, id_jogo=id_jogo, \
                            estatisticas=estatisticas, jogos=jogos, id_tipo_estatistica=id_tipo_estatistica)

@app.route('/contato', methods=['GET'])
@login_required
def pg_contato():
    msgs = MsgContato.query.filter_by(id_usuario=current_user.id)
    return render_template('contato.html', msgs=msgs)

@app.route('/jogos', methods=['GET'])
@login_required
def pg_jogos():
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    return render_template('jogos.html', jogos=jogos)

@app.route('/jogos/<id>', methods=['GET'])
@login_required
def pg_jogo(id=None):
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    jogo = Jogo.query.filter_by(id=id).first_or_404()
    estatisticas = Estatistica.query.filter_by(id_jogo=id).all()
    return render_template('jogos.html', jogos=jogos, jogo=jogo, estatisticas=estatisticas)

@app.route('/contato', methods=['POST'])
@login_required
def contato():
    assunto = request.form.get('assunto')
    mensagem = request.form.get('msg')
    msg = MsgContato(assunto=assunto, mensagem=mensagem, id_usuario=current_user.id)
    db.session.add(msg)
    db.session.commit()
    flash('Mensagem enviada com sucesso! Retornaremos o mais breve possível.', category='success')
    return redirect(url_for('pg_contato'))

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
