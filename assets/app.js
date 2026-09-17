const BASE_URL = window.location.origin.includes('github.dev') || window.location.origin.includes('app.github.dev')
    ? window.location.origin.replace('-3000.', '-5000.').replace('http://', 'https://')
    : 'http://127.0.0.1:5000';

const API_AUTH_URL = `${BASE_URL}/api/auth`;
const API_CHAMADOS_URL = `${BASE_URL}/api/chamados`;
const API_CARONAS_URL = `${BASE_URL}/api/caronas`;
const API_AVISOS_URL = `${BASE_URL}/api/avisos`;
const API_JARDINAGEM_URL = `${BASE_URL}/api/jardinagem`;

function lerCampo(...ids) {
    for (let id of ids) {
        const el = document.getElementById(id) || document.querySelector(`[name="${id}"]`);
        if (el && el.value !== undefined) return el.value.trim();
    }
    return '';
}

window.trocarPerfil = function(perfil) {
    const morador = document.getElementById('visao-morador') || document.getElementById('painel-morador');
    const sindico = document.getElementById('visao-sindico') || document.getElementById('painel-sindico');

    if (perfil === 'sindico' || perfil === 'admin') {
        if (sindico) sindico.style.display = 'block';
        if (morador) morador.style.display = 'none';
    } else if (perfil === 'morador') {
        if (sindico) sindico.style.display = 'none';
        if (morador) morador.style.display = 'block';
    } else {
        if (sindico) sindico.style.display = 'none';
        if (morador) morador.style.display = 'none';
    }
};

window.alternarTelaAuth = function(tela) {
    const authBox = document.getElementById('auth-container') || document.getElementById('box-login');
    const cadBox = document.getElementById('box-cadastro');
    if (authBox) authBox.style.display = (tela === 'cadastro') ? 'none' : 'block';
    if (cadBox) cadBox.style.display = (tela === 'cadastro') ? 'block' : 'none';
};

window.fazerLogout = function() {
    localStorage.clear();
    location.reload();
};

function aplicarPerfilSessao() {
    const usuarioSalvo = localStorage.getItem('condo_usuario');
    const authBox = document.getElementById('auth-container') || document.getElementById('box-login');
    const cadBox = document.getElementById('box-cadastro');

    if (!usuarioSalvo) {
        if (authBox) authBox.style.display = 'block';
        if (cadBox) cadBox.style.display = 'none';
        window.trocarPerfil('ocultar');
        return;
    }

    if (authBox) authBox.style.display = 'none';
    if (cadBox) cadBox.style.display = 'none';

    const usuario = JSON.parse(usuarioSalvo);
    const elNome = document.getElementById('nome-usuario');
    if (elNome) elNome.textContent = `${usuario.username} (${usuario.apartamento || 'Condomínio'})`;

    window.trocarPerfil(usuario.tipo);

    carregarChamados();
    carregarCaronas();
    carregarAvisos();
    carregarJardinagem();
}

// Processar Cadastro com captura dinâmica de campos
async function processarCadastro(e) {
    if (e) e.preventDefault();
    console.log(">>> Tentando cadastrar novo usuário...");

    const container = document.getElementById('box-cadastro') || document.getElementById('form-cadastro') || e.target;
    const inputs = container ? Array.from(container.querySelectorAll('input')) : [];

    let username = '', senha = '', apartamento = '';

    // 1. Busca inteligente por ID ou Name
    inputs.forEach(input => {
        const chave = (input.id || input.name || '').toLowerCase();
        if (chave.includes('user') || chave.includes('nome') || chave.includes('login')) username = input.value.trim();
        else if (chave.includes('senha') || chave.includes('pass')) senha = input.value.trim();
        else if (chave.includes('apto') || chave.includes('apartamento')) apartamento = input.value.trim();
    });

    // 2. Fallback caso os IDs não tenham nome padrão (pega por ordem)
    if (!username && inputs[0]) username = inputs[0].value.trim();
    if (!senha && inputs[1]) senha = inputs[1].value.trim();
    if (!apartamento && inputs[2]) apartamento = inputs[2].value.trim();

    console.log("Valores lidos do cadastro:", { username, senhaPreenchida: Boolean(senha), apartamento });

    if (!username || !senha) {
        alert("Preencha o nome do usuário e a senha.");
        return;
    }

    try {
        const res = await fetch(`${API_AUTH_URL}/cadastro`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, senha, apartamento })
        });

        const data = await res.json();
        console.log("Resposta do Cadastro:", res.status, data);

        if (res.ok) {
            alert("Conta criada com sucesso! Faça login.");
            window.alternarTelaAuth('login');
        } else {
            alert(data.erro || "Erro ao criar conta.");
        }
    } catch (err) {
        console.error("Erro no cadastro:", err);
        alert(`Erro de conexão: ${err.message}`);
    }
}

// CARREGAR DADOS
async function carregarChamados() {
    try {
        const res = await fetch(API_CHAMADOS_URL);
        const data = await res.json();
        const container = document.getElementById('lista-chamados') || document.getElementById('chamados-container');
        if (!container || !Array.isArray(data)) return;
        container.innerHTML = data.map(c => `<div class="card p-2 mb-2"><strong>Apto ${c.apartamento} - ${c.categoria}</strong><p>${c.descricao}</p></div>`).join('');
    } catch (e) {}
}

async function carregarCaronas() {
    try {
        const res = await fetch(API_CARONAS_URL);
        const data = await res.json();
        const container = document.getElementById('lista-caronas') || document.getElementById('caronas-container');
        if (!container || !Array.isArray(data)) return;
        container.innerHTML = data.map(c => `<div class="card p-2 mb-2"><strong>${c.motorista} (${c.apartamento})</strong><p>Destino: ${c.destino} - Horário: ${c.horario}</p></div>`).join('');
    } catch (e) {}
}

async function carregarAvisos() {
    try {
        const res = await fetch(API_AVISOS_URL);
        const data = await res.json();
        const container = document.getElementById('lista-avisos') || document.getElementById('avisos-container');
        if (!container || !Array.isArray(data)) return;
        container.innerHTML = data.map(a => `<div class="card p-2 mb-2"><strong>${a.titulo}</strong><p>${a.mensagem}</p></div>`).join('');
    } catch (e) {}
}

async function carregarJardinagem() {
    try {
        const res = await fetch(API_JARDINAGEM_URL);
        const data = await res.json();
        const container = document.getElementById('lista-jardinagem') || document.getElementById('jardinagem-container');
        if (!container || !Array.isArray(data)) return;
        container.innerHTML = data.map(j => `<div class="card p-2 mb-2"><strong>${j.atividade} (${j.data})</strong><p>${j.observacoes}</p></div>`).join('');
    } catch (e) {}
}

// EVENTOS DE SUBMIT E SALVAMENTO
document.addEventListener('DOMContentLoaded', () => {

    // Login
    const formLogin = document.getElementById('form-login') || document.querySelector('#auth-container form');
    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = lerCampo('login-username', 'username');
            const senha = lerCampo('login-senha', 'senha');
            if (!username || !senha) return alert("Preencha usuário e senha.");

            try {
                const res = await fetch(`${API_AUTH_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, senha })
                });
                const data = await res.json();
                if (res.ok && data.usuario) {
                    localStorage.setItem('condo_usuario', JSON.stringify(data.usuario));
                    aplicarPerfilSessao();
                } else {
                    alert(data.erro || "Credenciais incorretas.");
                }
            } catch (err) {
                alert("Erro ao conectar à API.");
            }
        });
    }

    // Cadastro de Morador
    const formCadastro = document.getElementById('form-cadastro') || document.querySelector('#box-cadastro form');
    if (formCadastro) {
        formCadastro.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = lerCampo('cad-username', 'username');
            const senha = lerCampo('cad-senha', 'senha');
            const apartamento = lerCampo('cad-apto', 'apartamento');

            if (!username || !senha) return alert("Preencha usuário e senha.");

            try {
                const res = await fetch(`${API_AUTH_URL}/cadastro`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, senha, apartamento })
                });
                const data = await res.json();
                if (res.ok) {
                    alert("Conta cadastrada com sucesso! Faça login.");
                    window.alternarTelaAuth('login');
                } else {
                    alert(data.erro || "Erro no cadastro.");
                }
            } catch (err) {
                alert("Erro de conexão com o servidor.");
            }
        });
    }

    // Jardinagem Submit
    const formJardinagem = document.getElementById('form-jardinagem') || document.querySelector('form[action*="jardinagem"]');
    if (formJardinagem) {
        formJardinagem.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                atividade: lerCampo('jard-atividade', 'atividade') || 'Poda',
                data: lerCampo('jard-data', 'data'),
                status: lerCampo('jard-status', 'status') || 'Agendado',
                observacoes: lerCampo('jard-obs', 'observacoes')
            };
            const res = await fetch(API_JARDINAGEM_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                alert("Agendamento de jardinagem salvo!");
                formJardinagem.reset();
                carregarJardinagem();
            }
        });
    }

    // Avisos Submit
    const formAviso = document.getElementById('form-aviso') || document.querySelector('form[action*="aviso"]');
    if (formAviso) {
        formAviso.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                titulo: lerCampo('aviso-titulo', 'titulo'),
                mensagem: lerCampo('aviso-mensagem', 'mensagem')
            };
            const res = await fetch(API_AVISOS_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                alert("Comunicado publicado com sucesso!");
                formAviso.reset();
                carregarAvisos();
            }
        });
    }

    aplicarPerfilSessao();
});