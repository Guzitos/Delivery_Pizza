
document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registrationForm');
    const messageDiv = document.getElementById('message');


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
                setTimeout(function() {
                  window.location.href = '/login';
                }, 1500)
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
});