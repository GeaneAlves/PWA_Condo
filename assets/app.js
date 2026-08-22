const API_URL = 'https://curly-acorn-g4rwqr97q497fxgq-5000.app.github.dev/api/jardinagem'; // Mantenha a sua URL da porta 5000

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
            
            // Renderiza as informações e os botões de ação
            li.innerHTML = `
                <div class="evento-info">
                    <span class="evento-data">📅 ${item.data}</span>
                    <strong>${item.atividade}</strong>
                    <p>${item.observacao || ''}</p>
                </div>
                <div class="evento-acoes">
                    <span class="badge ${item.status.toLowerCase().replace(/\s+/g, '-')}">${item.status}</span>
                    ${item.status !== 'Concluído' ? `<button class="btn-acao btn-concluir" onclick="concluirEvento(${item.id})">✅</button>` : ''}
                    <button class="btn-acao btn-excluir" onclick="excluirEvento(${item.id})">🗑️</button>
                </div>
            `;
            lista.appendChild(li);
        });
    } catch (erro) {
        console.error('Erro ao buscar dados:', erro);
        lista.innerHTML = '<li>Erro ao carregar os dados de manutenção do jardim.</li>';
    }
}

// Função para marcar como Concluído
async function concluirEvento(id) {
    try {
        const resposta = await fetch(`${API_URL}/${id}/concluir`, { method: 'PUT' });
        if (resposta.ok) {
            carregarJardinagem();
        } else {
            alert('Não foi possível atualizar o status.');
        }
    } catch (erro) {
        console.error('Erro ao concluir evento:', erro);
    }
}

// Função para Deletar
async function excluirEvento(id) {
    if (!confirm('Deseja realmente excluir este agendamento?')) return;

    try {
        const resposta = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        if (resposta.ok) {
            carregarJardinagem();
        } else {
            alert('Não foi possível excluir o registro.');
        }
    } catch (erro) {
        console.error('Erro ao excluir evento:', erro);
    }
}

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
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novoEvento)
            });

            if (resposta.ok) {
                alert('Manutenção cadastrada com sucesso!');
                formJardinagem.reset();
                carregarJardinagem();
            } else {
                alert('Erro ao salvar os dados no servidor.');
            }
        } catch (erro) {
            console.error('Erro na requisição POST:', erro);
            alert('Falha na comunicação com a API.');
        }
    });
}

document.addEventListener('DOMContentLoaded', carregarJardinagem);