# PWA_Condo
Tecnologia e Sustentabilidade: O Uso de PWAs para Otimizar os Processos e Convivência em Condomínios Residenciais e Fortalecer Microcomunidades.

condo-connect-pwa/
├── .gitignore
├── README.md
│
├── backend/                     # Servidor em Python (API Flask)
│   ├── app.py                   # Arquivo principal do servidor Flask
│   ├── requirements.txt         # Bibliotecas Python necessárias
│   ├── config.py                # Configurações do banco de dados e ambiente
│   ├── database.sql             # Scripts de criação do banco PostgreSQL
│   └── routes/                  # Rotas da API divididas por função
│       ├── __init__.py
│       ├── moradores.py
│       ├── chamados.py
│       ├── jardinagem.py        # API do Calendário de Jardinagem
│       └── caronas.py
│
└── frontend/                    # Interface PWA (Open no Navegador/Celular)
    ├── index.html               # Página inicial do aplicativo
    ├── manifest.json            # Configuração de instalação do PWA
    ├── sw.js                    # Service Worker (Cache offline/Instalação)
    │
    ├── assets/                  # Arquivos de mídia estáticos
    │   ├── css/
    │   │   └── style.css
    │   ├── js/
    │   │   ├── app.js           # Registro do Service Worker e lógica geral
    │   │   ├── api.js           # Funções de integração com o Python
    │   │   └── jardinagem.js    # Lógica do Calendário de Jardinagem
    │   └── icons/               # Ícones do PWA (192x192, 512x512)
    │       ├── icon-192.png
    │       └── icon-512.png
    │
    └── pages/                   # Telas secundárias da aplicação
        ├── sindico.html         # Painel administrativo do síndico
        ├── morador.html         # Feed e solicitações do morador
        ├── jardinagem.html      # Visualização do Calendário Verde
        └── faq.html             # Telefones e contatos úteis
