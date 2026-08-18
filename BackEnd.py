from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)      # link de acesso do Front End JavaScrip à API


# Substituir com a URL do  banco PostgreSQL real (local ou nuvem como Supabase/Neon/Render)
# Formato: postgresql://usuario:senha@host:porta/nome_do_banco

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.gymbtnuoahfpaqdwhwqj:Ltech*!9349@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Exemplo de como será a Tabela de Jardinagem
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
            "data": self.data_agendada.strftime('%y-%m-%d'),
            "status": self.status,
            "observacao": self.observacao
        }

# ROTAS DA API (aqui ficam a rota '/' e as outras rotas)
@app.route('/')
def home():
    return jsonify({"mensagem": "API do CondoConnect rodando com sucesso!"})

# Espaço onde serão listados todos os eventos
@app.route('/api/jardinagem', methods=['GET'])
def get_jardinagem():
    eventos = Jardinagem.query.order_by(Jardinagem.data_agendada.asc()).all()
    return jsonify([evento.to_dict() for evento in eventos])

# Espaço onde o Síndico um novo evento
@app.route('/api/jardinagem', methods=['POST'])
def add_jardinagem():
    dados = request.get_json()

    if not dados or not dados.get('atividade') or not dados.get('data'):
        return jsonify({"erro": "Atividade e data são obrigatórias!"}), 400

    novo_evento = Jardinagem(
        atividade=dados.get('atividade'),
        data_agendada=datetime.strptime(dados.get('data'), '%y-%m-%d').data(),
        status=dados.get('status', 'Agendado'),
        observacao=dados.get('observacao')
    )

    db.session.add(novo_evento)
    db.session.commit()


    return jsonify({
        "mensagem": "Evento cadastrado com sucesso!",
        "evento": novo_evento.to_dict()}), 201



# Rota inicial do calendário de jardinagem
# @app.route('/api/jardinagem', methods=['GET'])
# def get_jardinagem():
    # eventos = [
        # {"id": 1, "atividade": "Poda das árvores e arbustos", "data": # "2026-08-20", "status": "Agendado"}
        # {"id": 2, "atividade": "Adubação do jardim frontal", "data": # "2026-08-28", "status": "Agendado"}
     
    # ]
    # return jsonify(eventos)

if __name__ == '__main__':
    # criar as tabelas de forma automática no PostgreSQL
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5000)
