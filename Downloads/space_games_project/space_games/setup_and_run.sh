#!/usr/bin/env bash
# ============================================================
#  Space_Games — Script de Configuração e Execução
#  Executa tudo que você precisa para rodar o projeto
# ============================================================

set -e  # Para ao primeiro erro

echo ""
echo "🚀 ============================================"
echo "   SPACE_GAMES — Configuração do Projeto"
echo "============================================ 🚀"
echo ""

# 1. Cria e ativa ambiente virtual (opcional mas recomendado)
if [ ! -d "venv" ]; then
  echo "📦 Criando ambiente virtual..."
  python3 -m venv venv
fi

echo "⚡ Ativando ambiente virtual..."
source venv/bin/activate || source venv/Scripts/activate  # Windows/Linux

# 2. Instala dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt -q

# 3. Cria as migrações
echo "🗄️  Criando migrações..."
python manage.py makemigrations games

# 4. Aplica as migrações (cria o banco de dados)
echo "🏗️  Aplicando migrações..."
python manage.py migrate

# 5. Carrega os dados iniciais (categorias + jogos de exemplo)
echo "🎮 Carregando dados iniciais..."
python manage.py loaddata games/fixtures/initial_data.json

# 6. Cria superusuário padrão (admin/admin123)
echo "👤 Criando superusuário admin..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@spacegames.com', 'admin123')
    print('   ✅ Superusuário criado: admin / admin123')
else:
    print('   ℹ️  Superusuário já existe')
"

# 7. Coleta arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput -v 0 2>/dev/null || true

echo ""
echo "✅ ============================================"
echo "   Configuração concluída!"
echo "============================================"
echo ""
echo "  🌐 Servidor:    http://127.0.0.1:8000/"
echo "  🔧 Admin:       http://127.0.0.1:8000/admin/"
echo "  👤 Login admin: admin / admin123"
echo ""
echo "Iniciando servidor de desenvolvimento..."
echo ""

# 8. Inicia o servidor
python manage.py runserver
