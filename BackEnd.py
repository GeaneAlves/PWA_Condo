from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# Configuração do PostgreSQL Supabase (Pooler IPv4)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.gymbtnuoahfpaqdwhwqj:Ltech*!9349@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela Jardinagem
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

@app.route('/')
def home():
    return jsonify({"mensagem": "API do CondoConnect rodando com sucesso!"})

    # 2. Inserir nova manutenção pelo formulário (POST)
@app.route('/api/chamados', methods=['GET', 'POST'])
def gerenciar_chamados():
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
        
        return jsonify({"mensagem": "Chamado aberto com sucesso!", "chamado": novo_chamado.to_dict()}), 201

@app.route('/api/jardinagem/<int:id>/concluir', methods=['PUT', 'PATCH'])
def concluir_jardinagem(id):
    evento = Jardinagem.query.get_or_404(id)
    evento.status = 'Concluido'
    db.session.commit()
    return jsonify({"mensagem": "Status atualizado para Concluído!", "evento": evento.to_dict()}), 200

@app.route('/api/jardinagem/<int:id>', methods=['DELETE'])
def deletar_jardinagem(id):
    evento = Jardinagem.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"mensagem": "Evento removido com sucesso!"}), 200

# A classe chamado será inserida abaixo:

from datetime import date

class Chamado(db.Model):
    __tablename__ = 'chamados'
    
    id = db.Column(db.Integer, primary_key=True)
    apartamento = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), default='Média')
    status = db.Column(db.String(30), default='Aberto')
    data_abertura = db.Column(db.Date, nullable=True)

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
        
# rotas para o módulo de chamados
from datetime import date

@app.route('/api/chamados', methods=['GET', 'POST'])
def gerenciar_chamados():
    if request.method == 'GET':
        chamados = Chamado.query.order_by(Chamado.id.desc()).all()
        return jsonify([c.to_dict() for c in chamados]), 200

    if request.method == 'POST':
        dados = request.get_jason()
        if not dados or not dados.get('apartamento') or not dados.get('descricao'):
           return jsonify({"erro": "Apartamento e descrição são obrigatórios!"}), 400

        novo_chamado = Chamado(
            apartamento=dados.get('apartamento'),
            categoria=dados.get('categoria', 'Geral'),
            descricao=dados.get('descricao'),
            prioridade=dados.get('prioridade', 'Média'),
            status='Aberto',
            data_abertura=date.today()
        )
        db.session.add(novo_chamado)
        db.session.commit()
        return jsonify({"mensagem": "Chamado aberto com sucesso!", "chamado": novo_chamado.to_dict()}), 201

@app.route('/api/chamados/<int:id>/status', methods=['PUT', 'PATCH'])
def atualizar_status_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    dados = request.get_json()
    chamado.status = dados.get('status', 'Resolvido')
    db.session.commit()
    return jsonify({"mensagem": "Status do chamado atualizado!", "chamado": chamado.to_dict()}), 200

@app.route('/api/chamados/<int:id>', methods=['DELETE'])
def deletar_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    db.session.delete(chamado)
    db.session.commit()
    return jsonify({"mensagem": "Chamado removido com sucesso!"}), 200
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)