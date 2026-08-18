const API_URL = 'https://fantastic-space-sniffle-975495vj965jhp7q-5000.app.github.dev/api/jardinagem';

// Função para buscar e desenhar a lista
async function carregarJardinagem() {
    const lista = document.getElementById('lista-jardinagem');
    if (!lista) return;

    lista.innerHTML = '<li>Carregando agendamentos...</li>';

    try {
        const resposta = await fetch(API_URL);
        const eventos = await resposta.json();

        lista.innerHTML = '';

        if (!eventos || eventos.length === 0) {
            lista.innerHTML = '<li>Nenhuma atividade agendada no momento.</li>';
            return;
        }

        eventos.forEach(item => {
            const li = document.createElement('li');
            li.className = 'card-evento';
            li.innerHTML = `
                <div class="evento-info">
                    <span class="evento-data">📅 ${item.data}</span>
                    <strong>${item.atividade}</strong>
                    <p>${item.observacao || ''}</p>
                </div>
                <span class="badge">${item.status}</span>
            `;
            lista.appendChild(li);
        });
    } catch (erro) {
        console.error('Erro ao buscar dados:', erro);
        lista.innerHTML = '<li>Erro ao carregar os dados de manutenção do jardim.</li>';
    }
}

// Executa ao carregar a página
document.addEventListener('DOMContentLoaded', carregarJardinagem);

// Lógica de envio do formulário
const formJardinagem = document.getElementById('form-jardinagem');

if (formJardinagem) {
    formJardinagem.addEventListener('submit', async (event) => {
        event.preventDefault();

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
                formJardinagem.reset();
                carregarJardinagem(); // Atualiza a lista na hora
            } else {
                alert('Erro ao salvar os dados no servidor.');
            }
        } catch (erro) {
            console.error('Erro na requisição POST:', erro);
            alert('Falha na comunicação com a API.');
        }
    });
}