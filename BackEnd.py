from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def adicionar_headers_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///condoconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELOS
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), default='morador')
    apartamento = db.Column(db.String(30), nullable=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "tipo": self.tipo, "apartamento": self.apartamento}

class Chamado(db.Model):
    __tablename__ = 'chamados'
    id = db.Column(db.Integer, primary_key=True)
    apartamento = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), default='Média')
    status = db.Column(db.String(30), default='Aberto')

    def to_dict(self):
        return {"id": self.id, "apartamento": self.apartamento, "categoria": self.categoria, "descricao": self.descricao, "prioridade": self.prioridade, "status": self.status}

class Carona(db.Model):
    __tablename__ = 'caronas'
    id = db.Column(db.Integer, primary_key=True)
    motorista = db.Column(db.String(100), nullable=False)
    apartamento = db.Column(db.String(30), nullable=False)
    destino = db.Column(db.String(150), nullable=False)
    horario = db.Column(db.String(50), nullable=True)
    vagas = db.Column(db.Integer, default=1)
    whatsapp = db.Column(db.String(30), nullable=True)

    def to_dict(self):
        return {"id": self.id, "motorista": self.motorista, "apartamento": self.apartamento, "destino": self.destino, "horario": self.horario or 'A combinar', "vagas": self.vagas, "whatsapp": self.whatsapp or ''}

class Aviso(db.Model):
    __tablename__ = 'avisos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "mensagem": self.mensagem}

class Jardinagem(db.Model):
    __tablename__ = 'jardinagem'
    id = db.Column(db.Integer, primary_key=True)
    atividade = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), default='Agendado')
    observacoes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {"id": self.id, "atividade": self.atividade, "data": self.data, "status": self.status, "observacoes": self.observacoes or ''}

@app.route('/')
def home():
    return jsonify({"status": "API CondoConnect online", "porta": 5000})

# ROTAS AUTENTICAÇÃO
@app.route('/api/auth/cadastro', methods=['POST', 'OPTIONS'])
def cadastrar_usuario():
    if request.method == 'OPTIONS': 
        return jsonify({}), 200

    dados = request.get_json(silent=True) or request.form or {}
    username = str(dados.get('username', '') or dados.get('usuario', '')).strip()
    senha = str(dados.get('senha', '')).strip()
    apartamento = str(dados.get('apartamento', '') or dados.get('apto', '')).strip()

    print(f"\n[SOLICITACAO CADASTRO] Usuário: '{username}' | Apto: '{apartamento}'")

    if not username or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios!"}), 400

    usuario_existente = Usuario.query.filter(db.func.lower(Usuario.username) == username.lower()).first()
    if usuario_existente:
        return jsonify({"erro": "Este nome de usuário já está cadastrado!"}), 409

    try:
        novo = Usuario(username=username, tipo='morador', apartamento=apartamento or 'Geral')
        novo.set_senha(senha)
        db.session.add(novo)
        db.session.commit()
        print(f"[CADASTRO CONFIRMADO] Usuário '{username}' gravado com sucesso!\n")
        return jsonify({"mensagem": "Conta criada com sucesso!", "usuario": novo.to_dict()}), 201
    except Exception as err:
        db.session.rollback()
        print(f"[ERRO AO SALVAR] {err}\n")
        return jsonify({"erro": "Erro interno ao salvar no banco."}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def autenticar_usuario():
    if request.method == 'OPTIONS': return jsonify({}), 200
    dados = request.get_json(silent=True) or {}
    username = str(dados.get('username', '')).strip()
    senha = str(dados.get('senha', '')).strip()

    usuario = Usuario.query.filter(db.func.lower(Usuario.username) == username.lower()).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Usuário ou senha incorretos!"}), 401

    return jsonify({"mensagem": "Login OK", "usuario": usuario.to_dict()}), 200

# ROTAS RECURSOS
@app.route('/api/chamados', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_chamados():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        return jsonify([c.to_dict() for c in Chamado.query.order_by(Chamado.id.desc()).all()]), 200
    dados = request.get_json(silent=True) or {}
    novo = Chamado(
        apartamento=dados.get('apartamento', 'Geral'),
        categoria=dados.get('categoria', 'Geral'),
        descricao=dados.get('descricao', ''),
        prioridade=dados.get('prioridade', 'Média')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Chamado salvo!", "chamado": novo.to_dict()}), 201

@app.route('/api/caronas', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_caronas():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        return jsonify([c.to_dict() for c in Carona.query.order_by(Carona.id.desc()).all()]), 200
    dados = request.get_json(silent=True) or {}
    nova = Carona(
        motorista=dados.get('motorista', 'Morador'),
        apartamento=dados.get('apartamento', 'Condomínio'),
        destino=dados.get('destino', ''),
        horario=dados.get('horario', 'A combinar'),
        vagas=int(dados.get('vagas', 1)),
        whatsapp=dados.get('whatsapp', '')
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Carona salva!", "carona": nova.to_dict()}), 201

@app.route('/api/avisos', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_avisos():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        return jsonify([a.to_dict() for a in Aviso.query.order_by(Aviso.id.desc()).all()]), 200
    dados = request.get_json(silent=True) or {}
    novo = Aviso(titulo=dados.get('titulo', 'Aviso'), mensagem=dados.get('mensagem', ''))
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Aviso publicado!", "aviso": novo.to_dict()}), 201

@app.route('/api/jardinagem', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_jardinagem():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        return jsonify([j.to_dict() for j in Jardinagem.query.order_by(Jardinagem.id.desc()).all()]), 200
    dados = request.get_json(silent=True) or {}
    novo = Jardinagem(
        atividade=dados.get('atividade', 'Poda'),
        data=dados.get('data', ''),
        status=dados.get('status', 'Agendado'),
        observacoes=dados.get('observacoes', '')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Jardinagem agendada!", "jardinagem": novo.to_dict()}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(username='Admin').first():
            admin = Usuario(username='Admin', tipo='admin', apartamento='Administração')
            admin.set_senha('admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5000)