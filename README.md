# SpaceGames

Plataforma gamificada para descoberta e venda de jogos digitais.

## Arquitetura

```text
SpaceGames/
|
|-- Front-end/
|   `-- Angular + TypeScript
|       |-- Home
|       |-- Jogos
|       |-- Detalhes do jogo
|       |-- Login
|       |-- Perfil
|       `-- Carrinho
|
`-- Back-end/
    `-- Django + Django REST Framework
        |-- API
        |-- Usuários
        |-- Jogos
        |-- Categorias
        `-- Pedidos
```

No workspace, `Front-end/` contém a implementação Angular e `Back-end/` contém o projeto Django. O Angular é responsável pela experiência visual e navegação. O Django fornece a API REST, autenticação JWT, regras de negócio, persistência, mídia e painel administrativo.

## Executar

### Executar tudo (Windows)

Na raiz do projeto:

```powershell
./start-dev.ps1
```

O script abre o Django em `127.0.0.1:8000` e o Angular em `localhost:4200`. O proxy do Angular encaminha as chamadas `/api` e `/media` para o backend.

### Backend

```bash
cd Back-end
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### Frontend

Em outro terminal:

```bash
cd Front-end
npm install
npm start
```

Acesse `http://localhost:4200/`. O proxy Angular encaminha `/api` e `/media` para o Django em `127.0.0.1:8000`.
