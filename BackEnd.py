from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
# (mantenha os imports do SQLAlchemy e suas models aqui)

app = Flask(__name__)
CORS(app)

@app.route('/api/jardinagem', methods=['GET', 'POST'])
def gerenciar_jardinagem():
    # 1. Quando o Front-End PEDE a lista de dados (GET)
    if request.method == 'GET':
        eventos = Jardinagem.query.order_by(Jardinagem.data_agendada.asc()).all()
        return jsonify([
            {
                "id": e.id,
                "atividade": e.atividade,
                "data": e.data_agendada.strftime('%Y-%m-%d'),
                "status": e.status,
                "observacao": e.observacao
            } for e in eventos
        ]), 200

    # 2. Quando o Síndico ENVIA um novo agendamento (POST)
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
        
        return jsonify({"mensagem": "Evento cadastrado com sucesso!"}), 201