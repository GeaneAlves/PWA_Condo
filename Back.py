from flask import Flask, jsonify
from flask_cors import flask_cors

app = Flask(__name_)
CORS(app)      # link de acesso do Front End JavaScrip à API

@app.route('/')
def home():
    return jsonify({"status": "API do COndomínio rodando com sucesso!"})

# Rota inicial do calendário de jardinagem
@app.route('/api/jardinagem', methods=['GET'])
def get_jardinagem():
    eventos = [
        {"id": 1, "atividade": "Poda das árvores e arbustos", "data": "2026-08-20", "status": "Agendado"}
        {"id": 2, "atividade": "Adubação do jardim frontal", "data": "2026-08-28", "status": "Agendado"}
     
    ]
    return jsonify(eventos)

if __name_ == '__main__':
    app.run(debug=True, port=5000)
