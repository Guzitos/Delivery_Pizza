// Seu arquivo: Delivery_Pizza/Pizzaria/Guilherme/pycham/javascript/signin.js

document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registrationForm');
    const messageDiv = document.getElementById('message');
    const backToHomeButton = document.getElementById('backToHomeButton');


    const apiUrl = '/auth/create_account';

    if (!registrationForm) {
        console.error("Formulário de registro com ID 'registrationForm' não encontrado!");
        return;
    }

    registrationForm.addEventListener('submit', async(event) => {
        event.preventDefault();

        const formData = new FormData(registrationForm);
        const data = {
            nome: formData.get('nome'),
            email: formData.get('email'),
            senha: formData.get('senha'),
        };

        console.log('Dados a serem enviados:', data);

        try {
            messageDiv.textContent = 'Enviando...';
            messageDiv.className = 'message';

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            console.log('Resposta do backend:', result);

            if (response.ok) {
                messageDiv.textContent = `Sucesso: ${result.mensagem}`;
                messageDiv.className = 'message success';
                registrationForm.reset();
                window.location.href = '/login'; // Redireciona para o login após cadastro bem-sucedido
            } else {
                const errorMessage = result.detail || result.message || 'Erro desconhecido';
                messageDiv.textContent = `Erro: ${errorMessage}`;
                messageDiv.className = 'message error';
            }
        } catch (error) {
            console.error('Erro ao enviar dados:', error);
            messageDiv.textContent = `Erro de conexão: ${error.message}. Verifique o console para mais detalhes.`;
            messageDiv.className = 'message error';
        }
    });

    // LÓGICA DO BOTÃO "VOLTAR PARA A PÁGINA INICIAL"
    if (backToHomeButton){
        backToHomeButton.addEventListener('click',() => {
            window.location.href = '/';
        });
    } else {
        console.warn("Botão 'backToHomeButton' não encontrado no DOM. O redirecionamento não será ligado.");
    }
});