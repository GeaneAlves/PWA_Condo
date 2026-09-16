# PWA_Condo
Tecnologia e Sustentabilidade: O Uso de PWAs para Otimizar os Processos e Convivência em Condomínios Residenciais e Fortalecer Microcomunidades.



pip install -r requirements.txt

para criar outro codespace ou clonar o projeto em outra máquina.


O comando abaixo é para atualizar, instalar os pacotes para fazer rodar online
Tem de rodar o live view e atualizar no app.js os linkconst BASE_URL = 'https://-5000.app.github.dev';
const API_URL = `${BASE_URL}/api/jardinagem`;
const API_CHAMADOS_URL = `${BASE_URL}/api/chamados`;

python -m pip install flask flask-cors flask-sqlalchemy psycopg2-binary

Para rodar a API ==  python BackEnd.py

{Porta 3000 (Front-end) e a porta 5000 (Flask API) estejam com a visibilidade definida como Public. }

{Para inserir o link novo em todas as CONST do app.js, copia o link, seleciona o primeiro link do primeiro CONST, cola o link e Ctrl + Shift + L para selecionar tudo e colar.}

Instalar o módulo do Python para bibliotecas da mesma versão

python -c "from BackEnd import app, db; app.app_context().push(); db.create_all()"

Flask criar uma tabela e executar o script direto no terminal 




O que concluímos até aqui:
Modelagem da tabela no Supabase via PostgreSQL.

API RESTful em Flask com endpoints GET e POST unificados e CORS configurado. ok

Interface PWA reativa consumindo e enviando dados em tempo real.


Próximos Passos Sugeridos
Módulo de Chamados / Reparos: Criar uma nova seção ou aba para os moradores abrirem solicitações (ex: lâmpada queimada, vazamento) com status e prioridade. ok

Ajuste de Formatação de Data: Converter o formato YYYY-MM-DD para o padrão brasileiro DD/MM/AAAA na exibição dos cards.

Configuração PWA / Offline: Registrar o Service Worker (frontend.js / sw.js) para permitir a instalação do aplicativo no celular.

Opção 1: Adicionar o botão de Excluir ou Concluir direto nos cards de manutenção. ok

Opção 2: Criar o Módulo de Chamados/Reparos para os moradores abrirem solicitações com foto/descrição.

Opção 3: Ativar o recurso Offline/PWA instalável com o Service Worker no celular.