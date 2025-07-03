// Seu arquivo: Delivery_Pizza/Pizzaria/Guilherme/pycham/javascript/login.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');

    // **CORREÇÃO CRÍTICA AQUI:** A URL DEVE SER '/auth/login'
    const apiUrl = '/auth/login'; // Corresponde a prefixo /auth + rota /login

    if (!loginForm) {
        console.error("Formulário de login com ID 'loginForm' não encontrado!");
        return;
    }

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const data = {
            email: formData.get('email'),
            senha: formData.get('senha'),
        };

        console.log('Dados de login a serem enviados:', data);

        try {
            messageDiv.textContent = 'Verificando credenciais...';
            messageDiv.className = 'message';

            const response = await fetch(apiUrl, { // Usando a apiUrl corrigida
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            console.log('Resposta do backend:', result);

            if (response.ok) {
                const accessToken = result.access_token;
                const refreshToken = result.refresh_token;

                localStorage.setItem('access_token', accessToken);
                localStorage.setItem('refresh_token', refreshToken);

                messageDiv.textContent = `Login bem-sucedido! Bem-vindo(a)!`;
                messageDiv.className = 'message success';
                loginForm.reset();

                setTimeout(() => {
                    window.location.href = '/'; // Redireciona para uma página pós-login
                }, 1500);

            } else {
                const errorMessage = result.detail || result.message || 'Erro desconhecido';
                messageDiv.textContent = `Erro no login: ${errorMessage}`;
                messageDiv.className = 'message error';
            }
        } catch (error) {
            console.error('Erro ao tentar login:', error);
            messageDiv.textContent = `Erro de conexão: ${error.message}. Verifique o console para mais detalhes.`;
            messageDiv.className = 'message error';
        }
    });
});