# Guia de Implantação no PythonAnywhere

## 1. Preparação

### 1.1. Criar Conta
1. Acesse www.pythonanywhere.com
2. Clique em "Pricing & Signup"
3. Escolha o plano gratuito "Beginner"
4. Complete o registro

### 1.2. Preparar o Código
1. Certifique-se de que o repositório está no GitHub
2. O arquivo `requirements.txt` deve estar atualizado
3. Configure as variáveis de ambiente no `.env`
4. Teste a aplicação localmente

## 2. Configuração no PythonAnywhere

### 2.1. Criar Web App
1. Faça login no PythonAnywhere
2. Vá para a Dashboard
3. Clique em "Web" no menu superior
4. Clique em "Add a new web app"
5. Escolha seu domínio (guizera7.pythonanywhere.com)
6. Selecione "Flask" como framework
7. Escolha Python 3.9 como versão

### 2.2. Clonar o Repositório
1. Abra um console Bash no PythonAnywhere
2. Clone o repositório:
   ```bash
   git clone https://github.com/Guizera/frameworks_toledo.git
   ```

### 2.3. Configurar Ambiente Virtual
1. No console Bash, crie um ambiente virtual:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 venv
   ```
2. Ative o ambiente virtual:
   ```bash
   workon venv
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 2.4. Configurar a Web App
1. Na seção "Web", configure:
   - Source code: /home/guizera7/frameworks_toledo
   - Working directory: /home/guizera7/frameworks_toledo
   - Virtual environment: /home/guizera7/.virtualenvs/venv

2. Edite o arquivo WSGI:
   ```python
   import sys
   path = '/home/guizera7/frameworks_toledo'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

### 2.5. Configurar Variáveis de Ambiente
1. Na seção "Web", vá até "Environment variables"
2. Adicione as variáveis necessárias:
   - SECRET_KEY
   - FLASK_ENV
   - DATABASE_URL
   - Outras variáveis específicas

### 2.6. Configurar Banco de Dados MySQL

1. Na interface do PythonAnywhere:
   - Clique na aba "Databases"
   - Clique em "Create database" (nome será username$ecommerce)
   - Anote a senha gerada para o MySQL
   - Aguarde a criação do banco (pode levar alguns minutos)

2. Configure as variáveis de ambiente:
   - Na seção "Web", vá até "Environment variables"
   - Adicione as seguintes variáveis:
     ```
     DB_USERNAME=seu_username
     DB_PASSWORD=senha_gerada_mysql
     DB_HOST=seu_username.mysql.pythonanywhere-services.com
     DB_NAME=seu_username$ecommerce
     ```

3. No console Bash, instale o driver MySQL:
   ```bash
   cd frameworks_toledo
   workon venv
   pip install mysqlclient
   ```

4. Inicie o Python shell:
   ```bash
   python
   ```

5. No shell Python, crie as tabelas:
   ```python
   from app import db, app
   with app.app_context():
       db.create_all()
   ```

4. Para criar um usuário administrador (opcional):
   ```python
   from app import User
   from werkzeug.security import generate_password_hash
   
   admin = User(
       name='Admin',
       email='admin@example.com',
       password=generate_password_hash('sua-senha-aqui'),
       is_admin=True
   )
   
   with app.app_context():
       db.session.add(admin)
       db.session.commit()
   ```

5. Saia do shell Python:
   ```python
   exit()
   ```

## 3. Implantação

### 3.1. Arquivos Estáticos
1. Na seção "Web", configure:
   - Static files URL: /static/
   - Static files path: /home/guizera7/frameworks_toledo/static

### 3.2. Reload da Aplicação
1. Clique em "Reload" na seção "Web"
2. Aguarde a aplicação reiniciar

### 3.3. Verificação
1. Acesse o domínio (guizera7.pythonanywhere.com)
2. Teste todas as funcionalidades principais
3. Verifique os logs em caso de erro

## 4. Manutenção

### 4.1. Atualizações
1. No console Bash:
   ```bash
   cd frameworks_toledo
   git pull
   workon venv
   pip install -r requirements.txt
   ```
2. Clique em "Reload" na web app

### 4.2. Monitoramento
1. Verifique os logs de erro
2. Monitore o uso de recursos
3. Faça backups regulares do banco de dados

## 5. Solução de Problemas

### 5.1. Logs
- Error log: /var/log/guizera7.pythonanywhere.com.error.log
- Access log: /var/log/guizera7.pythonanywhere.com.access.log
- Server log: Seção "Web" > "Log files"

### 5.2. Problemas Comuns
1. **Erro 502 Bad Gateway**
   - Verifique o arquivo WSGI
   - Confira o ambiente virtual
   - Veja os logs de erro

2. **Arquivos Estáticos não Carregam**
   - Verifique as configurações de arquivos estáticos
   - Confira os caminhos dos arquivos
   - Teste as URLs estáticas

3. **Erro de Importação**
   - Verifique o PYTHONPATH
   - Confira as dependências
   - Teste o ambiente virtual

## 6. Link de Acesso

O sistema está disponível em:
https://guizera7.pythonanywhere.com

## 7. Justificativas

1. **Escolha do PythonAnywhere**
   - Hospedagem específica para Python
   - Configuração simplificada
   - Plano gratuito adequado
   - Suporte a Flask

2. **Ambiente Virtual**
   - Isolamento de dependências
   - Controle de versões
   - Evita conflitos
   - Facilita manutenção

3. **Configuração WSGI**
   - Padrão da indústria
   - Performance otimizada
   - Gerenciamento de processos
   - Logging adequado

4. **Variáveis de Ambiente**
   - Segurança de dados sensíveis
   - Configuração flexível
   - Separação de ambientes
   - Boas práticas de desenvolvimento

5. **Monitoramento**
   - Detecção rápida de problemas
   - Logs detalhados
   - Facilidade de debug
   - Manutenção proativa
