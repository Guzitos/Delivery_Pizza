# 🍕 Delivery_Pizza - Backend FastAPI

Este é um projeto backend de um sistema de delivery de pizzaria, desenvolvido com **FastAPI**. O sistema implementa funcionalidades básicas de autenticação e cadastro de usuários, servindo como base para a futura integração com pedidos e interface frontend.

## 🚀 Tecnologias utilizadas

- **Python 3.11**
- **FastAPI**
- **SQLite**
- **SQLAlchemy**
- **Uvicorn**
- **Pydantic**
- **Passlib** (para hash de senhas)
- **Python-Jose** (JWT)

## 📁 Estrutura do Projeto
Delivery_Pizza/

├── banco.db # Banco de dados SQLite

├── main.py # Arquivo principal da aplicação FastAPI

├── models.py # Modelos do banco de dados

├── schemas.py # Esquemas Pydantic (validação de dados)

├── auth.py # Lógica de autenticação e JWT

├── requirements.txt # Dependências do projeto

## ✅ Funcionalidades

- Cadastro de usuários
- Login com geração de token JWT
- Proteção de rotas autenticadas
- Integração com banco de dados SQLite

> 🔧 A ideia inicial do projeto era um sistema completo de pedidos de uma pizzaria, mas até o momento apenas a parte de autenticação e base do backend foi finalizada.

## ▶️ Como rodar o projeto localmente

1. Clone o repositório:

```
git clone https://github.com/Guzitos/Delivery_Pizza.git
cd Delivery_Pizza
```

2. Crie e ative um ambiente virtual:
```
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Execute a aplicação:
```
uvicorn main:app --reload
```

A API estará disponível em: http://127.0.0.1:8000

### 🧪 Testando a API
Acesse a documentação interativa gerada automaticamente pelo FastAPI:

Swagger UI: http://127.0.0.1:8000/docs

# 📌 Futuras implementações
Sistema de pedidos de pizza

Interface web frontend

Relacionamento entre usuários e pedidos

Integração com meios de pagamento

🤝 Contribuições
Contribuições são bem-vindas! Fique à vontade para abrir issues, pull requests ou entrar em contato.

### Desenvolvido com 💻 por Guzitos
