
const API_URL = 'https://fantastic-space-sniffle-975495vj965jhp7q-5000.app.github.dev/api/jardinagem'

async function carregarJardinagem() {
    const lista = document.getElementById('lista-jardinagem');
    if (!lista) return;

    lista.innerHTML = '<li>Carregando agendamentos...</li>';

    try {
        const resposta = await fetch(API_URL);
        const eventos = await resposta.json();

        lista.innerHTML = '';

        if (eventos.length === 0) {
            lista.innerHTML = '<li>Nenhuma atividade agendada no momento.</li>';
            return;
        }

        eventos.forEach(item => {
            const li = document.creatElement('li');
            li.className = 'card-evento';
            li.innerHTML = `
                <div class="evento-info">
                    <span class="data-evento">📅 ${item.data}</span>
                    <strong>${item.data}:</strong> ${item.atividade} - <em>(${item.status})</em>
                    <p>${item.observacao || ''}</p>
                </div>
                <span class="badge-status ${item.status.toLowerCase()}">${item.status}</span>
            `;
            lista.appendChild(li);
        });
    } catch (erro) {
        console.error('Erro ao buscar dados da API:', erro);
        lista.innerHTML = '<li>Não foi posível carregar a lista de manutenções.</li>';

    }
}

document.addEventListener('DOMContentLoaded', carregarJardinagem);