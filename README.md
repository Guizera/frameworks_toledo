# E-commerce Platform

Este é um projeto de e-commerce desenvolvido com Flask para a disciplina de Frameworks.

## Funcionalidades

- Sistema de usuários (cadastro e login)
- Gerenciamento de anúncios
- Categorização de produtos
- Sistema de perguntas e respostas
- Compra de produtos
- Lista de favoritos
- Relatórios de vendas e compras

## Estrutura do Projeto

```
trabalho_frameworks/
├── app.py              # Aplicação principal
├── models.py           # Modelos do banco de dados
├── requirements.txt    # Dependências do projeto
└── templates/         # Templates HTML
    └── base.html      # Template base
```

## Como executar

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse http://localhost:5000 no navegador

## Tecnologias Utilizadas

- Flask
- SQLAlchemy
- Flask-Login
- Bootstrap 5
- SQLite

## Modelo Entidade-Relacionamento (MER)

O MER do projeto está disponível no arquivo `docs/mer.png`.

## Diagrama de Navegação

O diagrama de navegação está disponível no arquivo `docs/navigation.png`. 