# 🚀🎮 Space Games

Sistema web desenvolvido em Django para gerenciamento e catálogo de jogos digitais.

## 📖 Sobre o Projeto

O Space Games é uma plataforma que permite visualizar, cadastrar e gerenciar jogos, categorias e informações relacionadas ao universo gamer. O projeto foi desenvolvido utilizando Django seguindo o padrão MVT (Model-View-Template).

## 🚀 Funcionalidades

- Cadastro de jogos
- Listagem de jogos
- Sistema de categorias
- Pesquisa de jogos
- Área administrativa do Django
- Sistema de favoritos
- Página de detalhes dos jogos
- Interface responsiva

## 🛠️ Tecnologias Utilizadas

- Python 3
- Django
- SQLite3
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Angular 20 (frontend standalone)

## 📂 Estrutura do Projeto

```text
SpaceGames/
│
├── frontend/
│   └── Angular + TypeScript
│       ├── Home
│       ├── Jogos
│       ├── Detalhes do jogo
│       ├── Login
│       ├── Perfil
│       └── Carrinho
│
└── space_games/
  └── Django + Django REST Framework
    ├── API
    ├── Usuários
    ├── Jogos
    ├── Categorias
    ├── Pedidos
    ├── media/
    ├── db.sqlite3
    ├── manage.py
    └── requirements.txt
```

O Angular concentra a experiência visual e consome os endpoints REST do Django. O Django permanece responsável por autenticação, regras de negócio, persistência, arquivos de jogos e painel administrativo.

## ⚙️ Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/space-games.git
```

### 2. Acessar a pasta do projeto

```bash
cd space-games
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

### 6. Executar migrações

```bash
python manage.py migrate
```

### 7. Iniciar servidor

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## 🎨 Frontend Angular

O catálogo Angular fica na pasta irmã `../Front-end` e consome a API REST do Django. Para executar a interface:

Terminal 1 (API Django):

```bash
python manage.py runserver
```

Terminal 2 (Angular):

```bash
cd ../Front-end
npm install
npm start
```

Acesse `http://localhost:4200/`. O Angular controla a home, pesquisa, login, cadastro, detalhes dos jogos, favoritos, carrinho e biblioteca. O proxy local encaminha `/api` e `/media` para o Django em `127.0.0.1:8000`.

Para gerar os arquivos de produção:

```bash
npm run build
```

## 👨‍💻 Autor

Marcos Eduardo de Oliveira Lima

## 📌 Melhorias Futuras

O projeto SpaceGames pode receber diversas melhorias e novos recursos futuramente, tornando a plataforma mais completa, segura e interativa.

- 🔐 **Sistema de login e autenticação de usuários**
- 🖼️ **Upload e gerenciamento de imagens dos jogos**
- 🔌 **API REST utilizando Django REST Framework**
- 🎮 **Sistema de gerenciamento de jogos**
- 🛒 **Carrinho de compras**
- 📥 **Download e instalação de jogos**
- ⚙️ **Painel administrativo avançado**
- ⭐ **Sistema de avaliações e favoritos**
- 🔎 **Melhoria no sistema de busca e filtros**
- 📱 **Otimização da interface para dispositivos móveis**
- 👤 **Perfil e histórico dos usuários**

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e de aprendizado.

##
<p align="center">
  <img src="https://media.tenor.com/KfL3l_4SuVEAAAAj/mario-super-mario-world.gif" width="200">
</p>