// URL base da sua API Flask (Porta 5000)
const BASE_URL = 'https://vigilant-system-975495vj9697274jq-5000.app.github.dev';

const API_AUTH_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/auth';
const API_JARDINAGEM_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/jardinagem';
const API_CHAMADOS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/chamados';
const API_AVISOS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/avisos';
const API_MORADORES_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/moradores';
const API_PRESTADORES_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/prestadores';
const API_ENCOMENDAS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/encomendas';
const API_PESQUISAS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/pesquisas';
const API_ACHADOS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/achados';
const API_CLASSIFICADOS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/classificados';
const API_CARONAS_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/caronas';

const API_URL = 'https://vigilant-system-975495vj9697274jq-3000.app.github.dev/api/jardinagem'; // Mantenha a sua URL da porta 5000

// ================= NAVEGAÇÃO E SESSÃO =================

function alternarTelaAuth(modo) {
    const formLogin = document.getElementById('form-login');
    const formCadastro = document.getElementById('form-cadastro');
    const titulo = document.getElementById('auth-titulo');

    if (!formLogin || !formCadastro || !titulo) return;

    if (modo === 'cadastro') {
        formLogin.style.display = 'none';
        formCadastro.style.display = 'block';
        titulo.innerText = 'Cadastro de Novo Morador';
    } else {
        formLogin.style.display = 'block';
        formCadastro.style.display = 'none';
        titulo.innerText = 'Acesso ao CondoConnect';
    }
}

function trocarPerfil(perfil) {
    const vMorador = document.getElementById('visao-morador');
    const vSindico = document.getElementById('visao-sindico');
    const btnM = document.getElementById('btn-perfil-morador');
    const btnS = document.getElementById('btn-perfil-sindico');

    if (perfil === 'morador') {
        if (vMorador) vMorador.style.display = 'block';
        if (vSindico) vSindico.style.display = 'none';
        if (btnM) btnM.classList.add('ativo');
        if (btnS) btnS.classList.remove('ativo');
        carregarAchados();
        carregarClassificados();
        carregarCaronas();
    } else {
        if (vMorador) vMorador.style.display = 'none';
        if (vSindico) vSindico.style.display = 'block';
        if (btnS) btnS.classList.add('ativo');
        if (btnM) btnM.classList.remove('ativo');
        carregarJardinagem();
        carregarChamados();
        carregarAvisos();
        carregarMoradores();
        carregarPrestadores();
        carregarEncomendas();
        carregarPesquisas();
    }
}

function fazerLogout() {
    localStorage.removeItem('condo_usuario');
    location.reload();
}

function aplicarPerfilSessao() {
    const usuarioLogado = JSON.parse(localStorage.getItem('condo_usuario') || 'null');
    const authContainer = document.getElementById('auth-container');
    const sessaoContainer = document.getElementById('usuario-sessao-container');
    const nomeUsuario = document.getElementById('nome-usuario-logado');
    const switcher = document.querySelector('.perfil-switcher');

    if (!usuarioLogado) {
        if (authContainer) authContainer.style.display = 'block';
        if (sessaoContainer) sessaoContainer.style.display = 'none';
        if (switcher) switcher.style.display = 'none';
        const vM = document.getElementById('visao-morador');
        const vS = document.getElementById('visao-sindico');
        if (vM) vM.style.display = 'none';
        if (vS) vS.style.display = 'none';
        return;
    }

    if (authContainer) authContainer.style.display = 'none';
    if (sessaoContainer) sessaoContainer.style.display = 'flex';
    if (nomeUsuario) nomeUsuario.innerText = `👤 ${usuarioLogado.username} (${usuarioLogado.tipo.toUpperCase()})`;
    if (switcher) switcher.style.display = 'flex';

    if (usuarioLogado.tipo === 'admin') {
        trocarPerfil('sindico');
    } else {
        trocarPerfil('morador');
    }
}

// Tornar funções disponíveis globalmente no HTML
window.alternarTelaAuth = alternarTelaAuth;
window.trocarPerfil = trocarPerfil;
window.fazerLogout = fazerLogout;

// Renderização de Jardinagem (com modo somente leitura para moradores)
async function carregarJardinagem() {
    try {
        const res = await fetch(API_JARDINAGEM_URL);
        const dados = await res.json();
        
        const listaSindico = document.getElementById('lista-jardinagem');
        const listaMorador = document.getElementById('lista-jardinagem-morador');

        const htmlSindico = (!dados || dados.length === 0) ? '<li>Nenhuma manutenção agendada.</li>' : dados.map(item => `
            <li class="card-evento">
                <div class="evento-info">
                    <span class="evento-data">📅 ${item.data}</span>
                    <strong>${item.atividade}</strong>
                    <p>${item.observacao || ''}</p>
                </div>
                <div class="evento-acoes">
                    <span class="badge ${item.status.toLowerCase().replace(/\s+/g, '-')}">${item.status}</span>
                    <button class="btn-acao btn-excluir" onclick="excluirJardinagem(${item.id})">🗑️</button>
                </div>
            </li>
        `).join('');

        const htmlMorador = (!dados || dados.length === 0) ? '<li>Nenhuma manutenção agendada no momento.</li>' : dados.map(item => `
            <li class="card-evento">
                <div class="evento-info">
                    <span class="evento-data">📅 ${item.data}</span>
                    <strong>${item.atividade}</strong>
                    <p>${item.observacao || ''}</p>
                </div>
                <div class="evento-acoes">
                    <span class="badge ${item.status.toLowerCase().replace(/\s+/g, '-')}">${item.status}</span>
                </div>
            </li>
        `).join('');

        if (listaSindico) listaSindico.innerHTML = htmlSindico;
        if (listaMorador) listaMorador.innerHTML = htmlMorador;
    } catch (e) {
        console.error('Erro ao buscar jardinagem:', e);
    }
}

// Renderização de Comunicados/Avisos
async function carregarAvisos() {
    try {
        const res = await fetch(API_AVISOS_URL);
        const dados = await res.json();

        const listaSindico = document.getElementById('lista-avisos');
        const listaMorador = document.getElementById('lista-avisos-morador');

        const htmlSindico = (!dados || dados.length === 0) ? '<li>Nenhum comunicado publicado.</li>' : dados.map(item => `
            <li class="card-evento card-aviso">
                <div class="evento-info">
                    <div style="display:flex; justify-content:space-between;"><span class="evento-data">📅 ${item.data_publicacao}</span><span class="badge">${item.tipo}</span></div>
                    <strong>${item.titulo}</strong>
                    <p>${item.mensagem}</p>
                    ${item.imagem ? `<div class="aviso-img-container"><img src="${item.imagem}" class="img-comunicado"></div>` : ''}
                </div>
                <div class="evento-acoes"><button class="btn-acao btn-excluir" onclick="excluirAviso(${item.id})">🗑️</button></div>
            </li>
        `).join('');

        const htmlMorador = (!dados || dados.length === 0) ? '<li>Nenhum comunicado do síndico.</li>' : dados.map(item => `
            <li class="card-evento card-aviso">
                <div class="evento-info">
                    <div style="display:flex; justify-content:space-between;"><span class="evento-data">📅 ${item.data_publicacao}</span><span class="badge">${item.tipo}</span></div>
                    <strong>${item.titulo}</strong>
                    <p>${item.mensagem}</p>
                    ${item.imagem ? `<div class="aviso-img-container"><img src="${item.imagem}" class="img-comunicado"></div>` : ''}
                </div>
            </li>
        `).join('');

        if (listaSindico) listaSindico.innerHTML = htmlSindico;
        if (listaMorador) listaMorador.innerHTML = htmlMorador;
    } catch (e) {
        console.error('Erro ao carregar avisos:', e);
    }
}

// Renderização de Prestadores de Serviço
async function carregarPrestadores() {
    try {
        const res = await fetch(API_PRESTADORES_URL);
        const dados = await res.json();

        const listaSindico = document.getElementById('lista-prestadores');
        const listaMorador = document.getElementById('lista-prestadores-morador');

        const htmlSindico = (!dados || dados.length === 0) ? '<li>Nenhum prestador ativo.</li>' : dados.map(p => `
            <li class="card-evento">
                <div class="evento-info"><strong>👷 ${p.nome}</strong> (${p.empresa_servico})<p>Destino: ${p.apartamento_destino}</p><small>Doc: ${p.documento}</small></div>
                <div class="evento-acoes"><button class="btn-acao btn-excluir" onclick="excluirPrestador(${p.id})">🗑️</button></div>
            </li>
        `).join('');

        const htmlMorador = (!dados || dados.length === 0) ? '<li>Nenhum prestador de serviço no momento.</li>' : dados.map(p => `
            <li class="card-evento">
                <div class="evento-info"><strong>👷 ${p.empresa_servico}</strong><p>Atendimento autorizado para: ${p.apartamento_destino}</p><small>📅 Data: ${p.data_registro}</small></div>
                <div class="evento-acoes"><span class="badge ${p.status_acesso.toLowerCase()}">${p.status_acesso}</span></div>
            </li>
        `).join('');

        if (listaSindico) listaSindico.innerHTML = htmlSindico;
        if (listaMorador) listaMorador.innerHTML = htmlMorador;
    } catch (e) {
        console.error('Erro ao carregar prestadores:', e);
    }
}

// Renderização de Moradores e Veículos
async function carregarMoradores() {
    try {
        const res = await fetch(API_MORADORES_URL);
        const dados = await res.json();

        const listaSindico = document.getElementById('lista-moradores');
        const listaMorador = document.getElementById('lista-moradores-morador');

        const htmlSindico = (!dados || dados.length === 0) ? '<li>Nenhum morador cadastrado.</li>' : dados.map(m => `
            <li class="card-evento">
                <div class="evento-info"><strong>👤 ${m.nome}</strong> (${m.apartamento})<p>🚗 Placa: ${m.placa_veiculo} | Vaga: ${m.vaga_garagem}</p></div>
                <div class="evento-acoes"><button class="btn-acao btn-excluir" onclick="excluirMorador(${m.id})">🗑️</button></div>
            </li>
        `).join('');

        const htmlMorador = (!dados || dados.length === 0) ? '<li>Nenhum registro disponível.</li>' : dados.map(m => `
            <li class="card-evento">
                <div class="evento-info"><strong>🏢 ${m.apartamento}</strong><p>🚗 Veículo: ${m.modelo_veiculo || ''} - <strong>${m.placa_veiculo}</strong> | 🅿️ Vaga: ${m.vaga_garagem}</p></div>
            </li>
        `).join('');

        if (listaSindico) listaSindico.innerHTML = htmlSindico;
        if (listaMorador) listaMorador.innerHTML = htmlMorador;
    } catch (e) {
        console.error('Erro ao carregar moradores:', e);
    }
}

async function carregarChamados() {
    const lista = document.getElementById('lista-chamados');
    if (!lista) return;
    try {
        const res = await fetch(API_CHAMADOS_URL);
        const dados = await res.json();
        lista.innerHTML = (!dados || dados.length === 0) ? '<li>Nenhum chamado pendente.</li>' : '';
        dados.forEach(item => {
            lista.innerHTML += `
                <li class="card-evento">
                    <div class="evento-info">
                        <span class="evento-data">📅 ${item.data_abertura} | 📍 <strong>${item.apartamento}</strong></span>
                        <p><strong>${item.categoria}:</strong> ${item.descricao}</p>
                        <small>Prioridade: ${item.prioridade}</small>
                    </div>
                    <div class="evento-acoes">
                        <span class="badge ${item.status.toLowerCase()}">${item.status}</span>
                        <button class="btn-acao btn-excluir" onclick="excluirChamado(${item.id})">🗑️</button>
                    </div>
                </li>
            `;
        });
    } catch (e) {
        lista.innerHTML = '<li>Erro ao carregar chamados.</li>';
    }
}

async function carregarEncomendas() {
    const lista = document.getElementById('lista-encomendas');
    if (!lista) return;
    try {
        const res = await fetch(API_ENCOMENDAS_URL);
        const dados = await res.json();
        lista.innerHTML = (!dados || dados.length === 0) ? '<li>Nenhuma encomenda pendente.</li>' : '';
        dados.forEach(e => {
            lista.innerHTML += `
                <li class="card-evento">
                    <div class="evento-info">
                        <strong>📦 Apt ${e.unidade}</strong> - ${e.tipo_pacote}
                        <p>Local: ${e.local_armazenado} | Status: ${e.status}</p>
                    </div>
                </li>
            `;
        });
    } catch (e) {
        lista.innerHTML = '<li>Erro ao carregar encomendas.</li>';
    }
}

async function carregarPesquisas() {
    const lista = document.getElementById('lista-pesquisas');
    if (!lista) return;
    try {
        const res = await fetch(API_PESQUISAS_URL);
        const dados = await res.json();
        if (dados.medias) {
            const elP = document.getElementById('media-pintura');
            const elJ = document.getElementById('media-jardim');
            const elL = document.getElementById('media-limpeza');
            const elA = document.getElementById('media-admin');
            if (elP) elP.innerText = dados.medias.pintura;
            if (elJ) elJ.innerText = dados.medias.jardim;
            if (elL) elL.innerText = dados.medias.limpeza;
            if (elA) elA.innerText = dados.medias.administracao;
        }
        lista.innerHTML = (!dados.avaliacoes || dados.avaliacoes.length === 0) ? '<li>Nenhuma avaliação enviada.</li>' : '';
        dados.avaliacoes.forEach(a => {
            lista.innerHTML += `
                <li class="card-evento">
                    <div class="evento-info">
                        <strong>🏠 ${a.apartamento}</strong> (📅 ${a.data_envio})
                        <p>Pintura: ${a.nota_pintura}⭐ | Jardim: ${a.nota_jardim}⭐ | Limpeza: ${a.nota_limpeza}⭐ | Admin: ${a.nota_administracao}⭐</p>
                    </div>
                </li>
            `;
        });
    } catch (e) {
        lista.innerHTML = '<li>Erro ao carregar pesquisas.</li>';
    }
}

async function carregarAchados() {
    const feed = document.getElementById('feed-achados');
    if (!feed) return;
    try {
        const res = await fetch(API_ACHADOS_URL);
        const dados = await res.json();
        feed.innerHTML = (!dados || dados.length === 0) ? '<p>Nenhum item achado no momento.</p>' : '';
        dados.forEach(i => {
            feed.innerHTML += `
                <div class="card-feed">
                    <div class="card-feed-corpo">
                        <h4>🔍 ${i.item}</h4>
                        <p>Local: ${i.local}</p>
                        <small>Contato: ${i.contato} | Status: ${i.status}</small>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        feed.innerHTML = '<p>Erro ao carregar achados.</p>';
    }
}

async function carregarClassificados() {
    const feed = document.getElementById('feed-classificados');
    if (!feed) return;
    try {
        const res = await fetch(API_CLASSIFICADOS_URL);
        const dados = await res.json();
        feed.innerHTML = (!dados || dados.length === 0) ? '<p>Nenhum item à venda.</p>' : '';
        dados.forEach(c => {
            feed.innerHTML += `
                <div class="card-feed">
                    <div class="card-feed-corpo">
                        <strong style="color: #16a34a;">${c.preco}</strong>
                        <h4>${c.titulo}</h4>
                        <p>${c.descricao}</p>
                        <small>Apto: ${c.apartamento}</small>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        feed.innerHTML = '<p>Erro ao carregar classificados.</p>';
    }
}

async function carregarCaronas() {
    const lista = document.getElementById('lista-caronas');
    if (!lista) return;
    try {
        const res = await fetch(API_CARONAS_URL);
        const dados = await res.json();
        lista.innerHTML = (!dados || dados.length === 0) ? '<li>Nenhuma oferta de carona.</li>' : '';
        dados.forEach(c => {
            lista.innerHTML += `
                <li class="card-evento">
                    <div class="evento-info">
                        <strong>🚗 Destino: ${c.destino}</strong>
                        <p>Horário: ${c.horario} | Vagas: ${c.vagas}</p>
                        <small>Motorista: ${c.motorista} (${c.apartamento})</small>
                    </div>
                </li>
            `;
        });
    } catch (e) {
        lista.innerHTML = '<li>Erro ao carregar caronas.</li>';
    }
}

// ================= LISTENERS DE FORMULÁRIO =================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Form de Login
    // Login
const formLogin = document.getElementById('form-login');
if (formLogin) {
    formLogin.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value.trim();
        const senha = document.getElementById('login-senha').value.trim();

        try {
            const res = await fetch(`${API_AUTH_URL}/login`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, senha })
            });

            const data = await res.json().catch(() => ({}));
            if (res.ok) {
                localStorage.setItem('condo_usuario', JSON.stringify(data.usuario));
                aplicarPerfilSessao();
            } else {
                alert(`Erro: ${data.erro || 'Falha no login'}`);
            }
        } catch (err) {
            console.error(err);
            alert('Falha na comunicação com a API.');
        }
    });
}

    // 2. Form de Cadastro de Morador
    const formCadastro = document.getElementById('form-cadastro');
    if (formCadastro) {
        formCadastro.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('cad-username').value.trim();
            const apartamento = document.getElementById('cad-apto').value.trim();
            const senha = document.getElementById('cad-senha').value.trim();

            if (senha.length !== 5 || isNaN(senha)) {
                alert('A senha do morador precisa ter exatamente 5 números.');
                return;
            }

            try {
                const res = await fetch(`${API_AUTH_URL}/cadastro`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, senha, apartamento })
                });
                const data = await res.json();
                if (res.ok) {
                    alert('Conta cadastrada com sucesso! Faça seu login.');
                    alternarTelaAuth('login');
                    formCadastro.reset();
                } else {
                    alert(`Erro: ${data.erro || 'Falha ao cadastrar'}`);
                }
            } catch (err) {
                alert('Falha na comunicação com a API.');
            }
        });
    }

    // 3. Form de Abertura de Chamado (Morador)
    const formChamado = document.getElementById('form-chamado');
    if (formChamado) {
        formChamado.addEventListener('submit', async (e) => {
            e.preventDefault();
            const novoChamado = {
                apartamento: document.getElementById('apartamento').value.trim(),
                categoria: document.getElementById('categoria').value,
                prioridade: document.getElementById('prioridade').value,
                descricao: document.getElementById('descricao-chamado').value.trim()
            };

            try {
                const res = await fetch(API_CHAMADOS_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(novoChamado)
                });
                if (res.ok) {
                    alert('Chamado registrado com sucesso!');
                    formChamado.reset();
                    carregarChamados();
                } else {
                    alert('Erro ao enviar o chamado.');
                }
            } catch (err) {
                alert('Falha na comunicação com o servidor.');
            }
        });
    }

    // 4. Form de Achados e Perdidos (Morador com Foto)
    const formAchado = document.getElementById('form-achado');
    if (formAchado) {
        formAchado.addEventListener('submit', async (e) => {
            e.preventDefault();
            const inputImg = document.getElementById('achado-img');
            let imgBase64 = null;

            if (inputImg.files && inputImg.files[0]) {
                imgBase64 = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(inputImg.files[0]);
                });
            }

            const item = {
                item: document.getElementById('achado-item').value.trim(),
                local: document.getElementById('achado-local').value.trim(),
                contato: document.getElementById('achado-contato').value.trim(),
                imagem: imgBase64
            };

            try {
                const res = await fetch(API_ACHADOS_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(item)
                });
                if (res.ok) {
                    alert('Item publicado no mural de achados!');
                    formAchado.reset();
                    carregarAchados();
                } else {
                    alert('Erro ao publicar item.');
                }
            } catch (err) {
                alert('Falha ao enviar dados.');
            }
        });
    }

    // 5. Form de Classificados / Bazar (Morador)
    const formClassificado = document.getElementById('form-classificado');
    if (formClassificado) {
        formClassificado.addEventListener('submit', async (e) => {
            e.preventDefault();
            const inputImg = document.getElementById('venda-img');
            let imgBase64 = null;

            if (inputImg.files && inputImg.files[0]) {
                imgBase64 = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(inputImg.files[0]);
                });
            }

            const produto = {
                titulo: document.getElementById('venda-titulo').value.trim(),
                preco: document.getElementById('venda-preco').value.trim(),
                apartamento: document.getElementById('venda-apto').value.trim(),
                telefone: document.getElementById('venda-tel').value.trim(),
                descricao: document.getElementById('venda-desc').value.trim(),
                imagem: imgBase64
            };

            try {
                const res = await fetch(API_CLASSIFICADOS_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(produto)
                });
                if (res.ok) {
                    alert('Anúncio publicado com sucesso!');
                    formClassificado.reset();
                    carregarClassificados();
                }
            } catch (err) {
                alert('Falha ao publicar anúncio.');
            }
        });
    }

    // 6. Form de Caronas (Morador)
    const formCarona = document.getElementById('form-carona');
    if (formCarona) {
        formCarona.addEventListener('submit', async (e) => {
            e.preventDefault();
            const carona = {
                motorista: document.getElementById('carona-motorista').value.trim(),
                apartamento: document.getElementById('carona-apto').value.trim(),
                destino: document.getElementById('carona-destino').value.trim(),
                horario: document.getElementById('carona-horario').value.trim(),
                vagas: document.getElementById('carona-vagas').value,
                contato: document.getElementById('carona-contato').value.trim()
            };

            try {
                const res = await fetch(API_CARONAS_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(carona)
                });
                if (res.ok) {
                    alert('Oferta de carona publicada!');
                    formCarona.reset();
                    carregarCaronas();
                }
            } catch (err) {
                alert('Falha ao registrar carona.');
            }
        });
    }

    // Inicia o estado da tela de acordo com o login
    aplicarPerfilSessao();
});