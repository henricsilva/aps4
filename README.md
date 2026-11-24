# API de Eventos Acadêmicos — APS 4 (Autenticação e Segurança)

API RESTful desenvolvida em Python com **FastAPI**, **SQLite**, **SQLAlchemy ORM** e **Pydantic**, evoluída com mecanismos de hashing de senhas (**Argon2** via `pwdlib`), autenticação baseada em **JWT** (`PyJWT`) e controle de acesso baseado em perfis (**RBAC**).

---

## 1. Estrutura do Projeto

```text
aps4_api_eventos/
├── main.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── model/
│   ├── __init__.py
│   └── usuario.py
├── schema/
│   ├── __init__.py
│   └── usuario_schema.py
├── service/
│   ├── __init__.py
│   ├── usuario_service.py
│   └── auth_service.py
├── security/
│   ├── __init__.py
│   ├── security.py
│   └── dependencies.py
└── controller/
    ├── __init__.py
    ├── usuario_controller.py
    └── auth_controller.py
```

---

## 2. Instalação e Execução

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente copiando `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

4. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```

5. Acesse a documentação interativa (Swagger UI):
   - `http://127.0.0.1:8000/docs`

---

## 3. Configuração da Chave Secreta e Administrador Inicial

A assinatura dos tokens JWT utiliza a variável de ambiente `JWT_SECRET_KEY`. Nunca publique chaves reais no repositório.

Exemplo de `.env`:
```env
JWT_SECRET_KEY=coloque_aqui_uma_chave_secreta_aleatoria_e_segura
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_INIT_EMAIL=admin@instituicao.edu.br
ADMIN_INIT_SENHA=Admin1234
ADMIN_INIT_NOME=Administrador Inicial
```

> **Criação controlada de administrador:** Ao iniciar a aplicação, se `ADMIN_INIT_EMAIL` e `ADMIN_INIT_SENHA` estiverem definidos no `.env`, a função `garantir_admin_inicial` cria o primeiro usuário com perfil `administrador` caso ele ainda não exista no banco. O endpoint público `POST /usuarios` cria exclusivamente usuários com perfil `usuario`.

---

## 4. Perfis e Permissões

| Perfil | Permissões |
| :--- | :--- |
| **`usuario`** | Consultar eventos e participantes conforme regras da APS 3; realizar inscrições em eventos; consultar seus próprios dados em `GET /auth/me`. |
| **`administrador`** | Todas as operações de `usuario`, além de cadastrar, atualizar e excluir eventos e consultar relatórios consolidados. |

---

## 5. Principais Rotas de Autenticação e Usuários

| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `POST` | `/usuarios` | Pública | Cadastra um novo usuário com perfil `usuario` e senha armazenada em hash Argon2. |
| `POST` | `/auth/login` | Pública | Autentica e-mail/senha e retorna um token JWT (`access_token`). |
| `GET` | `/auth/me` | Autenticada | Retorna os dados do usuário identificado pelo token JWT enviado no header `Authorization: Bearer <token>`. |

---

## 6. Exemplos de Uso e Roteiro de Testes no Swagger (`/docs`)

1. **Cadastrar usuário (`POST /usuarios`):**
   ```json
   {
     "nome": "Aluno Exemplo",
     "email": "aluno@exemplo.com",
     "senha": "senha_segura1"
   }
   ```
   - Retorno esperado: `201 Created` sem exibir `senha` ou `senha_hash`.
   - Repetir com o mesmo e-mail retorna `409 Conflict`.

2. **Login (`POST /auth/login`):**
   ```json
   {
     "email": "aluno@exemplo.com",
     "senha": "senha_segura1"
   }
   ```
   - Retorno esperado: `200 OK` com `access_token` e `token_type: "bearer"`.
   - Credenciais incorretas retornam `401 Unauthorized`.

3. **Autenticar no Swagger:**
   - Clique no botão **Authorize** no topo do `/docs` e cole o `access_token`.
   - Teste `GET /auth/me` (`200 OK`).
   - Teste rotas protegidas sem token ou com token inválido/expirado (`401 Unauthorized`).
   - Teste uma rota administrativa logado como `usuario` (`403 Forbidden`) e depois logado como `administrador` (`200 OK` / `201 Created`).
