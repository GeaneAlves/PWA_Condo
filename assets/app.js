
const API_URL = 'http://localhost:5000/api/jardinagem';

async function carregarJardinagem() {
    const lista = document.getElementById('lista-jardinagem');
    if (!lista) return;

    try {
        const resposta = await fetch(API_URL);
        const eventos = await resposta.json();

        lista.innerHTML = '';

        if (eventos.lenght === 0) {
            lista.innerHTML = '<li>Nenhuma atividade agendada no momento.</li>';
            return;
        }

        eventos.forEach(item => {
            const li = document.creatElement('li');
            li.innerHTML = `<strong>${item.data}:</strong> {item.atividade} - <em>(${item.status})</em>`;
            lista.appendChild(li);
        });
    } catch (erro) {
        console.error('Erro ao buscar dados da API:', erro);
        lista.innerHTML = '<li>Não foi posível carregar a lista de manutenções.</li>';

    }
}

document.addEventListener('DOMContentLoaded', carregarJardinagem);