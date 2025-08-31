# E-commerce Flask

Sistema de e-commerce desenvolvido com Flask para o trabalho da disciplina de Frameworks.

## Tecnologias Utilizadas

- Python 3.9+
- Flask 3.0.2
- SQLAlchemy 2.0.28
- Flask-Login 0.6.3
- Bootstrap 5.3.0

## Funcionalidades

- Sistema de autenticação e autorização
- CRUD completo de usuários
- Gerenciamento de categorias
- Sistema de anúncios
- Perguntas e respostas
- Sistema de compras
- Lista de favoritos
- Interface responsiva

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Guizera/frameworks_toledo
cd seu-repositorio
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados:
```bash
python
>>> from app import db
>>> db.create_all()
```

6. Execute a aplicação:
```bash
python app.py
```

## Estrutura do Projeto

```
trabalho_frameworks/
├── app.py              # Aplicação principal
├── models.py           # Modelos do banco de dados
├── requirements.txt    # Dependências
├── static/            # Arquivos estáticos
├── templates/         # Templates HTML
│   ├── ads/          # Templates de anúncios
│   ├── categories/   # Templates de categorias
│   ├── users/        # Templates de usuários
│   └── base.html     # Template base
└── docs/             # Documentação
```

## Rotas Protegidas

O sistema utiliza Flask-Login para proteger rotas que requerem autenticação. Consulte [docs/rotas_protegidas.md](docs/rotas_protegidas.md) para mais detalhes.

## Interface

A interface foi desenvolvida com Bootstrap 5.3.0, garantindo:
- Design responsivo
- Tema escuro consistente
- Componentes modernos
- Boa experiência do usuário

Mais detalhes em [docs/bootstrap_implementacao.md](docs/bootstrap_implementacao.md).

## Implantação

O sistema está implantado no PythonAnywhere. O guia completo de implantação está disponível em [docs/implantacao_pythonanywhere.md](docs/implantacao_pythonanywhere.md).

Acesse o sistema em: https://seu-usuario.pythonanywhere.com

## Desenvolvimento

1. Crie uma branch para sua feature:
```bash
git checkout -b feature/nova-funcionalidade
```

2. Faça commit das alterações:
```bash
git add .
git commit -m "Adiciona nova funcionalidade"
```

3. Envie para o GitHub:
```bash
git push origin feature/nova-funcionalidade
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas alterações
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

José Guilherme Alves da Cunha - [guizera7@gmail.com](mailto:guizera7@gmail.com)

