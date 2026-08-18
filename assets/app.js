// Lógica de aplicação PWA para gerenciar o cache e permitir que a aplicação funcione offline.
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

const formJardinagem = document.getElementById('form-jardinagem');

if (formJardinagem) {
    formJardinagem.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede a página de recarregar

        const novoEvento = {
            atividade: document.getElementById('atividade').value,
            data: document.getElementById('data').value,
            status: document.getElementById('status').value,
            observacao: document.getElementById('observacao').value
        };

        try {
            const resposta = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(novoEvento)
            });

            if (resposta.ok) {
                alert('Manutenção cadastrada com sucesso!');
                formJardinagem.reset(); // Limpa os campos
                carregarJardinagem();   // Recarrega a lista automaticamente na tela
            } else {
                alert('Erro ao salvar os dados no servidor.');
            }
        } catch (erro) {
            console.error('Erro na requisição POST:', erro);
            alert('Falha na comunicação com a API.');
        }
    });
}