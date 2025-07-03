// Seu arquivo: Delivery_Pizza/Pizzaria/Guilherme/pycham/templates/singin.js

document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registrationForm');
    const messageDiv = document.getElementById('message');

    // **IMPORTANTE:** A URL do backend é agora relativa ao domínio do servidor,
    // com o prefixo do APIRouter (/auth) e o caminho da rota (/criar_conta).
    const apiUrl = '/auth/criar_conta';

    if (!registrationForm) {
        console.error("Formulário de registro com ID 'registrationForm' não encontrado!");
        return; // Sai se o formulário não for encontrado
    }

    registrationForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // ESSA LINHA É CRÍTICA para impedir o GET padrão do formulário

        // Coleta os dados do formulário
        const formData = new FormData(registrationForm);
        const data = {
            nome: formData.get('nome'),
            email: formData.get('email'),
            senha: formData.get('senha'),
            // Se você descomentou os checkboxes no HTML, descomente e ajuste aqui:
            // ativo: formData.get('ativo') === 'on', // Checkbox retorna 'on' ou null
            // admin: formData.get('admin') === 'on'
        };

        // Opcional: Para depuração, veja o que está sendo enviado
        console.log('Dados a serem enviados:', data);

        try {
            messageDiv.textContent = 'Enviando...';
            messageDiv.className = 'message';

            // Faz a requisição POST para o endpoint do seu FastAPI
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Informa ao backend que estamos enviando JSON
                },
                body: JSON.stringify(data), // Converte o objeto JavaScript para uma string JSON
            });

            const result = await response.json(); // Pega a resposta JSON do backend
            console.log('Resposta do backend:', result); // Para depuração

            // Verifica se a requisição foi bem-sucedida (status 2xx)
            if (response.ok) {
                messageDiv.textContent = `Sucesso: ${result.mensagem}`;
                messageDiv.className = 'message success';
                registrationForm.reset(); // Limpa o formulário após o sucesso
                window.location.href = '/login'
            } else {
                // Se houve erro (ex: status 400, 422, 500), o FastAPI envia um JSON com 'detail'
                const errorMessage = result.detail || result.message || 'Erro desconhecido';
                messageDiv.textContent = `Erro: ${errorMessage}`;
                messageDiv.className = 'message error';
            }
        } catch (error) {
            // Erros de rede, problemas de conexão, etc.
            console.error('Erro ao enviar dados:', error);
            messageDiv.textContent = `Erro de conexão: ${error.message}. Verifique o console para mais detalhes.`;
            messageDiv.className = 'message error';
        }
    });
});