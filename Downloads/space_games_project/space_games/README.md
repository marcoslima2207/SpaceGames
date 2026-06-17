# 🚀 Space_Games

Sistema web de loja de games desenvolvido com **Python + Django**.

---

## 📋 Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 🏠 Página Inicial | Jogos em destaque, filtro por categoria, gratuitos |
| 🔍 Pesquisa | Busca por título, desenvolvedor ou categoria |
| ❤️ Favoritos | Salve seus jogos favoritos |
| 🛒 Carrinho | Adicione e finalize compras |
| 📚 Biblioteca | Seus jogos comprados/adquiridos |
| 🔐 Auth | Cadastro e login de usuários |
| 🔧 Admin | Painel administrativo completo |

---

## 🗄️ Banco de Dados (Tabelas)

```
Categoria  → id, nome, icone, slug
Jogo       → id, titulo, descricao, preco, gratuito, destaque, imagem, categoria_id, ...
Favorito   → id, usuario_id, jogo_id, data_adicionado
Carrinho   → id, usuario_id, jogo_id, quantidade, data_adicionado
Biblioteca → id, usuario_id, jogo_id, data_compra, preco_pago
```

---

## 🚀 Como Rodar

### Opção 1 — Script automático (Linux/Mac)

```bash
cd space_games
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Opção 2 — Passo a passo manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
# ou: venv\Scripts\activate    # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar e aplicar migrações
python manage.py makemigrations games
python manage.py migrate

# 4. Carregar dados iniciais (categorias + 12 jogos de exemplo)
python manage.py loaddata games/fixtures/initial_data.json

# 5. Criar superusuário para o admin
python manage.py createsuperuser
# ou use: python manage.py shell -c "
# from django.contrib.auth.models import User
# User.objects.create_superuser('admin', 'admin@email.com', 'admin123')"

# 6. Iniciar servidor
python manage.py runserver
```

### Acesso

| URL | Descrição |
|---|---|
| `http://127.0.0.1:8000/` | Página inicial |
| `http://127.0.0.1:8000/admin/` | Painel admin |
| `http://127.0.0.1:8000/login/` | Login |
| `http://127.0.0.1:8000/cadastro/` | Cadastro |
| `http://127.0.0.1:8000/biblioteca/` | Minha Biblioteca |
| `http://127.0.0.1:8000/favoritos/` | Meus Favoritos |
| `http://127.0.0.1:8000/carrinho/` | Carrinho |

---

## 🐘 Usar PostgreSQL (opcional)

Em `space_games/settings.py`, comente o bloco SQLite e descomente:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'space_games_db',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Instale também: `pip install psycopg2-binary`

---

## 📁 Estrutura do Projeto

```
space_games/
├── manage.py
├── requirements.txt
├── setup_and_run.sh
├── space_games/          ← Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── games/                ← App principal
│   ├── models.py         ← Tabelas do banco de dados
│   ├── views.py          ← Lógica de negócio
│   ├── urls.py           ← Rotas
│   ├── forms.py          ← Formulários
│   ├── admin.py          ← Painel administrativo
│   ├── context_processors.py
│   ├── fixtures/
│   │   └── initial_data.json  ← Dados de exemplo
│   └── templates/games/
│       ├── home.html
│       ├── detalhe_jogo.html
│       ├── login.html
│       ├── cadastro.html
│       ├── biblioteca.html
│       ├── favoritos.html
│       ├── carrinho.html
│       ├── pesquisa.html
│       └── _game_card.html
└── templates/
    └── base.html         ← Template base com navbar
```

---

## 🛠️ Tecnologias

- **Backend:** Python 3.11+ / Django 5.x
- **Banco de dados:** SQLite (padrão) / PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3
- **ORM:** Django ORM
- **Auth:** Django Auth System
- **Admin:** Django Admin customizado

---

## ⚙️ Adicionar Jogos

Via painel admin em `/admin/`:
1. Acesse **Categorias** → Adicione categorias
2. Acesse **Jogos** → Adicione jogos com imagem e preço

---

*Desenvolvido com 🚀 Python + Django*
