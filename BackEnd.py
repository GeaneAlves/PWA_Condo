from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

app = Flask(__name__)

# Liberação total de CORS para todas as origens, métodos e cabeçalhos
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def adicionar_headers_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    return response

# Configuração PostgreSQL Supabase (Pooler IPv4)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.gymbtnuoahfpaqdwhwqj:Ltech*!9349@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELOS ====================
class Jardinagem(db.Model):
    __tablename__ = 'jardinagem'
    id = db.Column(db.Integer, primary_key=True)
    atividade = db.Column(db.String(150), nullable=False)
    data_agendada = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Agendado')
    observacao = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "atividade": self.atividade,
            "data": self.data_agendada.strftime('%Y-%m-%d'),
            "status": self.status,
            "observacao": self.observacao
        }

class Chamado(db.Model):
    __tablename__ = 'chamados'
    id = db.Column(db.Integer, primary_key=True)
    apartamento = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), default='Média')
    status = db.Column(db.String(30), default='Aberto')
    data_abertura = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "apartamento": self.apartamento,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "prioridade": self.prioridade or 'Média',
            "status": self.status or 'Aberto',
            "data_abertura": self.data_abertura.strftime('%d/%m/%Y') if self.data_abertura else 'Recente'
        }

# ==================== ROTAS: JARDINAGEM ====================
@app.route('/')
def home():
    return jsonify({"mensagem": "API do CondoConnect rodando com sucesso!"})

@app.route('/api/jardinagem', methods=['GET', 'POST'])
def gerenciar_jardinagem():
    if request.method == 'GET':
        eventos = Jardinagem.query.order_by(Jardinagem.data_agendada.asc()).all()
        return jsonify([e.to_dict() for e in eventos]), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        if not dados.get('atividade') or not dados.get('data'):
            return jsonify({"erro": "Atividade e data são obrigatórias!"}), 400

        novo_evento = Jardinagem(
            atividade=dados.get('atividade'),
            data_agendada=datetime.strptime(dados.get('data'), '%Y-%m-%d').date(),
            status=dados.get('status', 'Agendado'),
            observacao=dados.get('observacao')
        )
        db.session.add(novo_evento)
        db.session.commit()
        return jsonify({"mensagem": "Evento cadastrado com sucesso!", "evento": novo_evento.to_dict()}), 201

@app.route('/api/jardinagem/<int:id>/concluir', methods=['PUT', 'PATCH'])
def concluir_jardinagem(id):
    evento = Jardinagem.query.get_or_404(id)
    evento.status = 'Concluído'
    db.session.commit()
    return jsonify({"mensagem": "Status atualizado!", "evento": evento.to_dict()}), 200

@app.route('/api/jardinagem/<int:id>', methods=['DELETE'])
def deletar_jardinagem(id):
    evento = Jardinagem.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"mensagem": "Evento removido!", "id": id}), 200

# ==================== ROTAS: CHAMADOS ====================
@app.route('/api/chamados', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_chamados():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        chamados = Chamado.query.order_by(Chamado.id.desc()).all()
        return jsonify([c.to_dict() for c in chamados]), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        apartamento = dados.get('apartamento')
        descricao = dados.get('descricao')

        if not apartamento or not descricao:
            return jsonify({"erro": "Apartamento e descrição são obrigatórios!"}), 400

        novo_chamado = Chamado(
            apartamento=apartamento,
            categoria=dados.get('categoria', 'Geral'),
            descricao=descricao,
            prioridade=dados.get('prioridade', 'Média'),
            status='Aberto',
            data_abertura=date.today()
        )
        db.session.add(novo_chamado)
        db.session.commit()
        return jsonify({"mensagem": "Chamado registrado com sucesso!", "chamado": novo_chamado.to_dict()}), 201

@app.route('/api/chamados/<int:id>/status', methods=['PUT', 'PATCH'])
def atualizar_status_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    chamado.status = 'Resolvido'
    db.session.commit()
    return jsonify({"mensagem": "Status do chamado atualizado!", "chamado": chamado.to_dict()}), 200

@app.route('/api/chamados/<int:id>', methods=['DELETE'])
def deletar_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    db.session.delete(chamado)
    db.session.commit()
    return jsonify({"mensagem": "Chamado removido!", "id": id}), 200

# ==================== MODELO: AVISOS ====================
class Aviso(db.Model):
    __tablename__ = 'avisos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), default='Geral') # Ex: Importante, Urgente, Manutenção, Assembleia
    imagem = db.Column(db.Text, nullable=True)        # Armazena URL ou Base64 da imagem
    data_publicacao = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "tipo": self.tipo or 'Geral',
            "imagem": self.imagem,
            "data_publicacao": self.data_publicacao.strftime('%d/%m/%Y') if self.data_publicacao else 'Recente'
        }

# ==================== ROTAS: AVISOS ====================
@app.route('/api/avisos', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_avisos():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        avisos = Aviso.query.order_by(Aviso.id.desc()).all()
        return jsonify([a.to_dict() for a in avisos]), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        titulo = dados.get('titulo')
        mensagem = dados.get('mensagem')

        if not titulo or not mensagem:
            return jsonify({"erro": "Título e mensagem são obrigatórios!"}), 400

        novo_aviso = Aviso(
            titulo=titulo,
            mensagem=mensagem,
            tipo=dados.get('tipo', 'Geral'),
            imagem=dados.get('imagem'),
            data_publicacao=date.today()
        )
        db.session.add(novo_aviso)
        db.session.commit()
        return jsonify({"mensagem": "Aviso publicado com sucesso!", "aviso": novo_aviso.to_dict()}), 201

@app.route('/api/avisos/<int:id>', methods=['DELETE', 'OPTIONS'])
def deletar_aviso(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    aviso = Aviso.query.get_or_404(id)
    db.session.delete(aviso)
    db.session.commit()
    return jsonify({"mensagem": "Aviso removido!", "id": id}), 200

# ==================== MODELO: MORADORES & VEÍCULOS ====================
class Morador(db.Model):
    __tablename__ = 'moradores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    apartamento = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    vaga_garagem = db.Column(db.String(20), nullable=True)
    placa_veiculo = db.Column(db.String(10), nullable=True)
    modelo_veiculo = db.Column(db.String(50), nullable=True)
    observacao_seguranca = db.Column(db.Text, nullable=True) # Ex: Autorizado para receber encomendas, restrição de acesso, etc.

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "apartamento": self.apartamento,
            "telefone": self.telefone or '',
            "vaga_garagem": self.vaga_garagem or 'Sem vaga',
            "placa_veiculo": self.placa_veiculo or 'Sem veículo',
            "modelo_veiculo": self.modelo_veiculo or '',
            "observacao_seguranca": self.observacao_seguranca or ''
        }

# ==================== ROTAS: MORADORES & VEÍCULOS ====================
@app.route('/api/moradores', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_moradores():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        moradores = Morador.query.order_by(Morador.apartamento.asc()).all()
        return jsonify([m.to_dict() for m in moradores]), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        nome = dados.get('nome')
        apartamento = dados.get('apartamento')

        if not nome or not apartamento:
            return jsonify({"erro": "Nome e Apartamento são obrigatórios!"}), 400

        novo_morador = Morador(
            nome=nome,
            apartamento=apartamento,
            telefone=dados.get('telefone'),
            vaga_garagem=dados.get('vaga_garagem'),
            placa_veiculo=dados.get('placa_veiculo', '').upper().strip(),
            modelo_veiculo=dados.get('modelo_veiculo'),
            observacao_seguranca=dados.get('observacao_seguranca')
        )
        db.session.add(novo_morador)
        db.session.commit()
        return jsonify({"mensagem": "Morador e veículo cadastrados com sucesso!", "morador": novo_morador.to_dict()}), 201

@app.route('/api/moradores/<int:id>', methods=['DELETE', 'OPTIONS'])
def deletar_morador(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    morador = Morador.query.get_or_404(id)
    db.session.delete(morador)
    db.session.commit()
    return jsonify({"mensagem": "Registro removido!", "id": id}), 200

# ==================== MODELO: PRESTADORES DE SERVIÇO ====================
class Prestador(db.Model):
    __tablename__ = 'prestadores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    documento = db.Column(db.String(30), nullable=False) # RG ou CPF
    empresa_servico = db.Column(db.String(100), nullable=False) # Ex: Vivo Fibra, Eletricista particular
    apartamento_destino = db.Column(db.String(50), nullable=False) # Ex: Ap 104 - Bloco A ou Área Comum
    telefone = db.Column(db.String(30), nullable=True)
    status_acesso = db.Column(db.String(30), default='Liberado') # Liberado, Finalizado, Bloqueado
    data_registro = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "documento": self.documento,
            "empresa_servico": self.empresa_servico,
            "apartamento_destino": self.apartamento_destino,
            "telefone": self.telefone or '',
            "status_acesso": self.status_acesso or 'Liberado',
            "data_registro": self.data_registro.strftime('%d/%m/%Y') if self.data_registro else 'Hoje'
        }

# ==================== ROTAS: PRESTADORES DE SERVIÇO ====================
@app.route('/api/prestadores', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_prestadores():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        prestadores = Prestador.query.order_by(Prestador.id.desc()).all()
        return jsonify([p.to_dict() for p in prestadores]), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        nome = dados.get('nome')
        documento = dados.get('documento')
        empresa_servico = dados.get('empresa_servico')
        apartamento_destino = dados.get('apartamento_destino')

        if not nome or not documento or not empresa_servico or not apartamento_destino:
            return jsonify({"erro": "Nome, Documento, Serviço e Destino são obrigatórios!"}), 400

        novo_prestador = Prestador(
            nome=nome,
            documento=documento,
            empresa_servico=empresa_servico,
            apartamento_destino=apartamento_destino,
            telefone=dados.get('telefone'),
            status_acesso='Liberado',
            data_registro=date.today()
        )
        db.session.add(novo_prestador)
        db.session.commit()
        return jsonify({"mensagem": "Prestador registrado com sucesso!", "prestador": novo_prestador.to_dict()}), 201

@app.route('/api/prestadores/<int:id>/status', methods=['PUT', 'PATCH', 'OPTIONS'])
def atualizar_status_prestador(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    prestador = Prestador.query.get_or_404(id)
    dados = request.get_json(silent=True) or {}
    prestador.status_acesso = dados.get('status', 'Finalizado')
    db.session.commit()
    return jsonify({"mensagem": "Status de acesso atualizado!", "prestador": prestador.to_dict()}), 200

@app.route('/api/prestadores/<int:id>', methods=['DELETE', 'OPTIONS'])
def deletar_prestador(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    prestador = Prestador.query.get_or_404(id)
    db.session.delete(prestador)
    db.session.commit()
    return jsonify({"mensagem": "Registro de prestador removido!", "id": id}), 200

# ==================== MODELO: ENCOMENDAS / CAIXA DE CORREIO ====================
class Encomenda(db.Model):
    __tablename__ = 'encomendas'

    id = db.Column(db.Integer, primary_key=True)
    unidade = db.Column(db.String(10), nullable=False) # Ex: 101, 204, 408
    tipo_pacote = db.Column(db.String(80), nullable=False) # Ex: Correspondência, Caixa Pequena, Shopee/Mercado Livre
    codigo_rastreio = db.Column(db.String(50), nullable=True)
    local_armazenado = db.Column(db.String(80), default="Caixa de Correio") # Caixa de Correio ou Portaria
    status = db.Column(db.String(30), default='Disponível') # Disponível, Retirado
    data_chegada = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "unidade": self.unidade,
            "tipo_pacote": self.tipo_pacote,
            "codigo_rastreio": self.codigo_rastreio or 'Sem rastreio',
            "local_armazenado": self.local_armazenado,
            "status": self.status,
            "data_chegada": self.data_chegada.strftime('%d/%m/%Y') if self.data_chegada else 'Hoje'
        }

# ==================== ROTAS: ENCOMENDAS ====================
@app.route('/api/encomendas', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_encomendas():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        encomendas = Encomenda.query.order_by(Encomenda.id.desc()).all()
        return jsonify([e.to_dict() for e in encomendas]), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        unidade = dados.get('unidade')
        tipo_pacote = dados.get('tipo_pacote')

        if not unidade or not tipo_pacote:
            return jsonify({"erro": "Unidade e tipo de pacote são obrigatórios!"}), 400

        nova_encomenda = Encomenda(
            unidade=unidade,
            tipo_pacote=tipo_pacote,
            codigo_rastreio=dados.get('codigo_rastreio'),
            local_armazenado=dados.get('local_armazenado', 'Caixa de Correio'),
            status='Disponível',
            data_chegada=date.today()
        )
        db.session.add(nova_encomenda)
        db.session.commit()
        return jsonify({"mensagem": "Entrega registrada com sucesso!", "encomenda": nova_encomenda.to_dict()}), 201

@app.route('/api/encomendas/<int:id>/retirar', methods=['PUT', 'PATCH', 'OPTIONS'])
def retirar_encomenda(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    encomenda = Encomenda.query.get_or_404(id)
    encomenda.status = 'Retirado'
    db.session.commit()
    return jsonify({"mensagem": "Status alterado para Retirado!", "encomenda": encomenda.to_dict()}), 200

@app.route('/api/encomendas/<int:id>', methods=['DELETE', 'OPTIONS'])
def deletar_encomenda(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    encomenda = Encomenda.query.get_or_404(id)
    db.session.delete(encomenda)
    db.session.commit()
    return jsonify({"mensagem": "Registro de entrega excluído!", "id": id}), 200

# ==================== MODELO: PESQUISA DE SATISFAÇÃO ====================
class PesquisaSatisfacao(db.Model):
    __tablename__ = 'pesquisa_satisfacao'

    id = db.Column(db.Integer, primary_key=True)
    apartamento = db.Column(db.String(20), nullable=False)
    nota_pintura = db.Column(db.Integer, nullable=False)      # 1 a 5
    nota_jardim = db.Column(db.Integer, nullable=False)       # 1 a 5
    nota_limpeza = db.Column(db.Integer, nullable=False)      # 1 a 5
    nota_administracao = db.Column(db.Integer, nullable=False)# 1 a 5
    comentario = db.Column(db.Text, nullable=True)
    data_envio = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "apartamento": self.apartamento,
            "nota_pintura": self.nota_pintura,
            "nota_jardim": self.nota_jardim,
            "nota_limpeza": self.nota_limpeza,
            "nota_administracao": self.nota_administracao,
            "comentario": self.comentario or '',
            "data_envio": self.data_envio.strftime('%d/%m/%Y') if self.data_envio else 'Recente'
        }

# ==================== ROTAS: PESQUISA DE SATISFAÇÃO ====================
@app.route('/api/pesquisas', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_pesquisas():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        avaliacoes = PesquisaSatisfacao.query.order_by(PesquisaSatisfacao.id.desc()).all()
        total = len(avaliacoes)
        
        # Cálculo de médias consolidadas para o painel do síndico
        if total > 0:
            media_pintura = round(sum(a.nota_pintura for a in avaliacoes) / total, 1)
            media_jardim = round(sum(a.nota_jardim for a in avaliacoes) / total, 1)
            media_limpeza = round(sum(a.nota_limpeza for a in avaliacoes) / total, 1)
            media_admin = round(sum(a.nota_administracao for a in avaliacoes) / total, 1)
        else:
            media_pintura = media_jardim = media_limpeza = media_admin = 0.0

        return jsonify({
            "total_respostas": total,
            "medias": {
                "pintura": media_pintura,
                "jardim": media_jardim,
                "limpeza": media_limpeza,
                "administracao": media_admin
            },
            "avaliacoes": [a.to_dict() for a in avaliacoes]
        }), 200

    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        apartamento = dados.get('apartamento')

        if not apartamento:
            return jsonify({"erro": "O apartamento é obrigatório!"}), 400

        nova_avaliacao = PesquisaSatisfacao(
            apartamento=apartamento,
            nota_pintura=int(dados.get('nota_pintura', 5)),
            nota_jardim=int(dados.get('nota_jardim', 5)),
            nota_limpeza=int(dados.get('nota_limpeza', 5)),
            nota_administracao=int(dados.get('nota_administracao', 5)),
            comentario=dados.get('comentario'),
            data_envio=date.today()
        )
        db.session.add(nova_avaliacao)
        db.session.commit()
        return jsonify({"mensagem": "Avaliação enviada com sucesso!", "avaliacao": nova_avaliacao.to_dict()}), 201

@app.route('/api/pesquisas/<int:id>', methods=['DELETE', 'OPTIONS'])
def deletar_pesquisa(id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    avaliacao = PesquisaSatisfacao.query.get_or_404(id)
    db.session.delete(avaliacao)
    db.session.commit()
    return jsonify({"mensagem": "Registro de avaliação removido!", "id": id}), 200

# ==================== MODELOS DO MORADOR ====================

class AchadoPerdido(db.Model):
    __tablename__ = 'achados_perdidos'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120), nullable=False)
    local_encontrado = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    contato_morador = db.Column(db.String(60), nullable=False) # Ex: Ap 204
    imagem = db.Column(db.Text, nullable=True) # Base64
    status = db.Column(db.String(30), default='Disponível') # Disponível, Devolvido
    data_registro = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "item": self.item,
            "local": self.local_encontrado,
            "descricao": self.descricao or '',
            "contato": self.contato_morador,
            "imagem": self.imagem,
            "status": self.status,
            "data": self.data_registro.strftime('%d/%m/%Y') if self.data_registro else ''
        }

class Classificado(db.Model):
    __tablename__ = 'classificados'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.String(30), nullable=False) # Ex: R$ 50,00
    descricao = db.Column(db.Text, nullable=True)
    apartamento = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    imagem = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Disponível') # Disponível, Vendido
    data_publicacao = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "preco": self.preco,
            "descricao": self.descricao or '',
            "apartamento": self.apartamento,
            "telefone": self.telefone,
            "imagem": self.imagem,
            "status": self.status,
            "data": self.data_publicacao.strftime('%d/%m/%Y') if self.data_publicacao else ''
        }

class Carona(db.Model):
    __tablename__ = 'caronas'
    id = db.Column(db.Integer, primary_key=True)
    motorista = db.Column(db.String(100), nullable=False)
    apartamento = db.Column(db.String(30), nullable=False)
    destino = db.Column(db.String(120), nullable=False)
    horario_dias = db.Column(db.String(100), nullable=False) # Ex: Seg a Sex às 07:30
    vagas = db.Column(db.Integer, default=2)
    contato = db.Column(db.String(30), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "motorista": self.motorista,
            "apartamento": self.apartamento,
            "destino": self.destino,
            "horario": self.horario_dias,
            "vagas": self.vagas,
            "contato": self.contato
        }

# ==================== ROTAS DO MORADOR ====================

# Achados e Perdidos
@app.route('/api/achados', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_achados():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        itens = AchadoPerdido.query.order_by(AchadoPerdido.id.desc()).all()
        return jsonify([i.to_dict() for i in itens]), 200
    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        novo = AchadoPerdido(
            item=dados.get('item'),
            local_encontrado=dados.get('local'),
            descricao=dados.get('descricao'),
            contato_morador=dados.get('contato'),
            imagem=dados.get('imagem')
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({"mensagem": "Item registrado!", "item": novo.to_dict()}), 201

@app.route('/api/achados/<int:id>/devolver', methods=['PUT', 'OPTIONS'])
def devolver_achado(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    item = AchadoPerdido.query.get_or_404(id)
    item.status = 'Devolvido'
    db.session.commit()
    return jsonify({"mensagem": "Item marcado como devolvido!"}), 200

# Classificados / Desapego
@app.route('/api/classificados', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_classificados():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        itens = Classificado.query.order_by(Classificado.id.desc()).all()
        return jsonify([i.to_dict() for i in itens]), 200
    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        novo = Classificado(
            titulo=dados.get('titulo'),
            preco=dados.get('preco'),
            descricao=dados.get('descricao'),
            apartamento=dados.get('apartamento'),
            telefone=dados.get('telefone'),
            imagem=dados.get('imagem')
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({"mensagem": "Anúncio publicado!", "item": novo.to_dict()}), 201

@app.route('/api/classificados/<int:id>/vender', methods=['PUT', 'OPTIONS'])
def vender_classificado(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    item = Classificado.query.get_or_404(id)
    item.status = 'Vendido'
    db.session.commit()
    return jsonify({"mensagem": "Item marcado como vendido!"}), 200

# Caronas Solidárias
@app.route('/api/caronas', methods=['GET', 'POST', 'OPTIONS'])
def gerenciar_caronas():
    if request.method == 'OPTIONS': return jsonify({}), 200
    if request.method == 'GET':
        caronas = Carona.query.order_by(Carona.id.desc()).all()
        return jsonify([c.to_dict() for c in caronas]), 200
    if request.method == 'POST':
        dados = request.get_json(silent=True) or {}
        nova = Carona(
            motorista=dados.get('motorista'),
            apartamento=dados.get('apartamento'),
            destino=dados.get('destino'),
            horario_dias=dados.get('horario'),
            vagas=int(dados.get('vagas', 1)),
            contato=dados.get('contato')
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({"mensagem": "Carona disponibilizada!", "carona": nova.to_dict()}), 201

from werkzeug.security import generate_password_hash, check_password_hash

# ==================== MODELO: USUÁRIOS ====================
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), default='morador') # 'admin' ou 'morador'
    apartamento = db.Column(db.String(30), nullable=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "tipo": self.tipo,
            "apartamento": self.apartamento
        }

# ==================== ROTAS DE AUTENTICAÇÃO ====================
@app.route('/api/auth/cadastro', methods=['POST', 'OPTIONS'])
def cadastrar_usuario():
    if request.method == 'OPTIONS': return jsonify({}), 200

    dados = request.get_json(silent=True) or {}
    username = dados.get('username', '').strip()
    senha = str(dados.get('senha', '')).strip()
    apartamento = dados.get('apartamento', '').strip()

    if not username or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios!"}), 400

    if len(senha) != 5 or not senha.isdigit():
        return jsonify({"erro": "A senha do morador deve conter exatamente 5 dígitos numéricos!"}), 400

    if Usuario.query.filter_by(username=username).first():
        return jsonify({"erro": "Este nome de usuário já está em uso!"}), 409

    novo_usuario = Usuario(
        username=username,
        tipo='morador',
        apartamento=apartamento
    )
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Conta criada com sucesso!", "usuario": novo_usuario.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def autenticar_usuario():
    if request.method == 'OPTIONS': return jsonify({}), 200

    dados = request.get_json(silent=True) or {}
    username = dados.get('username', '').strip()
    senha = str(dados.get('senha', '')).strip()

    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Usuário ou senha inválidos!"}), 401

    return jsonify({
        "mensagem": "Login realizado com sucesso!",
        "usuario": usuario.to_dict()
    }), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Cria o Admin padrão caso não exista
        admin_padrao = Usuario.query.filter_by(username='Admin').first()
        if not admin_padrao:
            admin = Usuario(username='Admin', tipo='admin', apartamento='Administração')
            admin.set_senha('admin')
            db.session.add(admin)
            db.session.commit()
            print("Usuário Admin padrão criado com sucesso!")
    app.run(debug=True, port=5000)