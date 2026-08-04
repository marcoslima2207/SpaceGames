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

## 📂 Estrutura do Projeto

```text
space_games/
│
├── games/
├── usuarios/
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

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

## 👨‍💻 Autor

Marcos Eduardo de Oliveira Lima

## 📌 Melhorias Futuras

- Sistema de avaliações
- Upload de imagens dos jogos
- API REST com Django REST Framework
- Sistema de recomendações
- Carrinho de compras
- Download/instalação de jogos
- Dashboard administrativo avançado

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e de aprendizado.

