from flask import Flask, render_template, request, redirect, flash, \
    send_from_directory, url_for, abort
from flask_login import LoginManager, login_user, logout_user, current_user, \
    login_required
import os
from models import db, MsgFormIndex, MsgContato, Usuario, TipoEstatistica, \
    Estatistica, Jogador, Jogo, Chart, Clube, EsquemaTatico, Modulo
import random
from functools import wraps

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'pg_index'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Você deve logar para acessar esta página.'

def login_required(role="ANY"):
    def login_wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
               return login_manager.unauthorized()
            urole = current_user.get_role().nome
            if ( (urole != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return login_wrapper

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo=nome_arquivo)

def chartEstatisticas(estatisticas):
    labels = []
    values = []
    colors = []
    if estatisticas:
        tipo_estatistica = estatisticas[0].tipo_estatistica.nome
    else:
        tipo_estatistica = ''
    for e in estatisticas:
        labels.append(e.jogador.nome)
        values.append(e.quantidade)
        c = lambda: random.randint(0,255)
        colors.append('#%02X%02X%02X' % (c(), c(), c()))
    return Chart(labels, values, colors, tipo_estatistica)

@app.route('/', methods=['GET'])
def pg_index():
    if current_user.is_authenticated:
        return redirect(url_for('pg_dashboard'))
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
@login_required(role="ANY")
def pg_dashboard():
    return render_template('dashboard.html')

@app.route('/desempenho-fisico', methods=["GET", "POST"])
@login_required(role="ANY")
def pg_desempenho_fisico():
    tipos_estatistica = TipoEstatistica.query.filter_by(id_modulo=1)
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    estatisticas = []
    id_tipo_estatistica = None
    id_jogo = None
    chart = []
    if request.method == 'POST':
        id_jogo = int(request.form['id_jogo'])
        id_tipo_estatistica = int(request.form['id_tipo_estatistica'])

        if id_tipo_estatistica != None:
            estatisticas = Estatistica.query \
                                    .filter_by(id_tipo_estatistica=id_tipo_estatistica) \
                                    .join(Jogo) \
                                    .filter_by(id_time=current_user.id_clube, id=id_jogo) \
                                    .all()
            chart = chartEstatisticas(estatisticas)
    else:
        id_tipo_estatistica = request.args.get('id_tipo_estatistica')
    return render_template('desempenho-fisico.html', tipos_estatistica=tipos_estatistica, id_jogo=id_jogo, \
                            estatisticas=estatisticas, jogos=jogos, id_tipo_estatistica=id_tipo_estatistica, chart=chart)

@app.route('/desempenho-tecnico', methods=['GET', 'POST'])
@login_required(role="ANY")
def pg_desempenho_tecnico():
    tipos_estatistica = TipoEstatistica.query.filter_by(id_modulo=2)
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    estatisticas = []
    id_tipo_estatistica = None
    id_jogo = None
    chart = []
    if request.method == 'POST':
        id_jogo = int(request.form['id_jogo'])
        id_tipo_estatistica = int(request.form['id_tipo_estatistica'])

        if id_tipo_estatistica != None:
            estatisticas = Estatistica.query \
                                    .filter_by(id_tipo_estatistica=id_tipo_estatistica) \
                                    .join(Jogo) \
                                    .filter_by(id_time=current_user.id_clube, id=id_jogo) \
                                    .all()

            chart = chartEstatisticas(estatisticas)
    else:
        id_tipo_estatistica = request.args.get('id_tipo_estatistica')
    return render_template('desempenho-tecnico.html', tipos_estatistica=tipos_estatistica, id_jogo=id_jogo, \
                            estatisticas=estatisticas, jogos=jogos, id_tipo_estatistica=id_tipo_estatistica, \
                            chart=chart)

@app.route('/desempenho-tatico', methods=['GET', 'POST'])
@login_required(role="ANY")
def pg_desempenho_tatico():
    tipos_estatistica = TipoEstatistica.query.filter_by(id_modulo=3)
    jogos = Jogo.query.filter_by(id_time=current_user.clube.id).all()
    estatisticas = []
    id_tipo_estatistica = None
    jogo = None
    if request.method == 'POST':
        jogo = Jogo.query.filter_by(id=int(request.form['id_jogo'])).first()
        id_tipo_estatistica = request.form['id_tipo_estatistica']

        if id_tipo_estatistica != None:
            estatisticas = Estatistica.query \
                                    .filter_by(id_tipo_estatistica=id_tipo_estatistica) \
                                    .join(Jogo) \
                                    .filter_by(id_time=current_user.id_clube, id=jogo.id) \
                                    .all()
    else:
        id_tipo_estatistica = request.args.get('id_tipo_estatistica')
    return render_template('desempenho-tatico.html', tipos_estatistica=tipos_estatistica, jogo=jogo, \
                            estatisticas=estatisticas, jogos=jogos, id_tipo_estatistica=id_tipo_estatistica)

@app.route('/contato', methods=['GET'])
@login_required(role="ANY")
def pg_contato():
    msgs = MsgContato.query.filter_by(id_usuario=current_user.id)
    return render_template('contato.html', msgs=msgs)

@app.route('/contato', methods=['POST'])
@login_required(role="ANY")
def contato():
    assunto = request.form.get('assunto')
    mensagem = request.form.get('msg')
    msg = MsgContato(assunto=assunto, mensagem=mensagem, id_usuario=current_user.id)
    db.session.add(msg)
    db.session.commit()
    flash('Mensagem enviada com sucesso! Retornaremos o mais breve possível.', category='success')
    return redirect(url_for('pg_contato'))

@app.route('/cadastrar', methods=['GET'])
@login_required(role="ADMIN")
def pg_cadastrar():
    return render_template('cadastrar.html')

@app.route('/cadastrar/jogador', methods=['GET'])
@login_required(role="ADMIN")
def pg_cadastro_jogador():
    clubes = Clube.query.all()
    return render_template('cadastrar.html', rend_cadastro_jogador=True, clubes=clubes)

@app.route('/cadastrar/jogador', methods=['POST'])
@login_required(role="ADMIN")
def cadastrar_jogador():
    nome = str(request.form['nome'])
    idade = int(request.form['idade'])
    id_clube = int(request.form['id_clube'])
    altura = request.form['altura']
    peso = request.form['peso']
    if altura:
        altura = int(altura)
    else:
        altura = None
    if peso:
        peso = int(peso)
    else:
        peso = None
    try:
        jogador = Jogador(nome, idade, id_clube, altura, peso)
        db.session.add(jogador)
        db.session.commit()
        flash('Jogador cadastrado com sucesso!', category='success')
    except:
        flash('Erro desconhecido ao cadastrar jogador.', category='danger')
    return redirect(url_for('pg_cadastro_jogador'))

@app.route('/cadastrar/jogo', methods=['GET'])
@login_required(role="ADMIN")
def pg_cadastro_jogo():
    clubes = Clube.query.all()
    esquemas_taticos = EsquemaTatico.query.all()
    return render_template('cadastrar.html', rend_cadastro_jogo=True, clubes=clubes, \
                                esquemas_taticos=esquemas_taticos)

@app.route('/cadastrar/jogo', methods=['POST'])
@login_required(role="ADMIN")
def cadastrar_jogo():
    data = request.form['data']
    local = int(request.form['local'])
    id_time = int(request.form['id_time'])
    id_adversario = int(request.form['id_adversario'])
    placar_time = request.form['placar_time']
    placar_adversario = request.form['placar_adversario']
    id_esquema_tatico = int(request.form['id_esquema_tatico'])

    if placar_time != None and placar_adversario != None:
        try:
            placar_time = int(placar_time)
            placar_adversario = int(placar_adversario)
        except:
            flash('Digite somente números nos campos do placar!', category='danger')
            return redirect(url_for('pg_cadastro_jogo'))

    if id_time == id_adversario:
        flash('Um clube não pode jogar contra si mesmo!', category='danger')
        return redirect(url_for('pg_cadastro_jogo'))

    try:
        jogo = Jogo(data=data, local=local, id_time=id_time, id_adversario=id_adversario, \
                        placar_time=placar_time, placar_adversario=placar_adversario, \
                        id_esquema_tatico=id_esquema_tatico)
        db.session.add(jogo)
        db.session.commit()
        flash('Jogo cadastrado com sucesso!', category='success')
    except:
        flash('Erro desconhecido ao cadastrar jogo.', category='danger')
    return redirect(url_for('pg_cadastro_jogo'))

@app.route('/cadastrar/tipo-estatistica', methods=['GET'])
@login_required(role="ADMIN")
def pg_cadastro_tipo_estatistica():
    modulos = Modulo.query.all()
    return render_template('cadastrar.html', rend_cadastro_tipo_estatistica=True, \
                            modulos=modulos)

@app.route('/cadastrar/tipo-estatistica', methods=['POST'])
@login_required(role="ADMIN")
def cadastrar_tipo_estatistica():
    nome = request.form['nome']
    id_modulo = int(request.form['id_modulo'])
    unidade_medida = request.form['unidade_medida']

    try:
        tipo_estatistica = TipoEstatistica(nome=nome, id_modulo=id_modulo, \
                                unidade_medida=unidade_medida)
        db.session.add(tipo_estatistica)
        db.session.commit()
        flash('Tipo de estatística cadastrada com sucesso!', category='success')
    except:
        flash('Erro desconhecido ao cadastrar tipo de estatística.', category='danger')
    return redirect(url_for('pg_cadastro_tipo_estatistica'))

@app.route('/cadastrar/estatistica', methods=['GET'])
@login_required(role="ADMIN")
def pg_cadastro_estatistica():
    id_clube = request.args.get('id_clube')
    if id_clube == None:
        clubes = Clube.query.all()
        return render_template('cadastrar.html', rend_cadastro_estatistica_clube=True, \
                                    clubes=clubes)
    else:
        jogadores = Jogador.query.filter_by(id_clube=id_clube).all()
        jogos = Jogo.query.filter_by(id_time=id_clube).all()
        tipos_estatistica = TipoEstatistica.query.all()
        return render_template('cadastrar.html', rend_cadastro_estatistica=True, \
            jogadores=jogadores, jogos=jogos, tipos_estatistica=tipos_estatistica)

@app.route('/cadastrar/estatistica', methods=['POST'])
@login_required(role="ADMIN")
def cadastrar_estatistica():
    id_jogo = int(request.form['id_jogo'])
    id_jogador = int(request.form['id_jogador'])
    id_tipo_estatistica = int(request.form['id_tipo_estatistica'])
    quantidade = request.form['quantidade']

    try:
        estatistica = Estatistica(id_jogo=id_jogo, id_jogador=id_jogador, \
                id_tipo_estatistica=id_tipo_estatistica, quantidade=quantidade)
        db.session.add(estatistica)
        db.session.commit()
        flash('Estatística cadastrada com sucesso!', category='success')
    except:
        flash('Erro desconhecido ao cadastrar estatística.', category='danger')
    return redirect(url_for('pg_cadastro_estatistica'))

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
