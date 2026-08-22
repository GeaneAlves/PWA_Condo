from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

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

@app.route('/api/jardinagem', methods=['GET', 'POST'])
def gerenciar_jardinagem():
    # 1. Buscar lista de manutenções (GET)
    if request.method == 'GET':
        eventos = Jardinagem.query.order_by(Jardinagem.data_agendada.asc()).all()
        return jsonify([e.to_dict() for e in eventos]), 200

    # 2. Inserir nova manutenção pelo formulário (POST)
    if request.method == 'POST':
        dados = request.get_json()
        
        if not dados or not dados.get('atividade') or not dados.get('data'):
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
    evento.status = 'Concluido'
    db.session.commit()
    return jsonify({"mensagem": "Status atualizado para Concluído!", "evento": evento.to_dict()}), 200

@app.route('/api/jardinagem/<int:id>', methods=['DELETE'])
def deletar_jardinagem(id):
    evento = Jardinagem.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"mensagem": "Evento removido com sucesso!"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)