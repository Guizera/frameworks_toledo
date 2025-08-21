# Documentação de Implementação do E-commerce

## Introdução

Este documento descreve as implementações realizadas no sistema de e-commerce desenvolvido com Flask, justificando as decisões técnicas tomadas com base nas aulas apresentadas.

## Arquitetura do Sistema

O sistema foi desenvolvido seguindo o padrão MVC (Model-View-Controller), que é uma das melhores práticas para desenvolvimento web:

- **Models**: Implementados em `models.py`, representam as entidades do sistema e suas relações
- **Views**: Templates HTML em Jinja2, organizados por funcionalidade
- **Controllers**: Rotas implementadas em `app.py`

### Justificativa
O padrão MVC foi escolhido por:
- Separar claramente as responsabilidades do código
- Facilitar a manutenção e evolução do sistema
- Permitir o reuso de componentes
- Seguir as boas práticas apresentadas nas aulas

## Banco de Dados

Utilizamos SQLAlchemy como ORM (Object-Relational Mapping) para:
- Mapear objetos Python para tabelas do banco de dados
- Gerenciar relacionamentos entre entidades
- Garantir a integridade dos dados
- Facilitar as operações CRUD

### Justificativa
O uso de ORM:
- Aumenta a produtividade no desenvolvimento
- Reduz a complexidade do código
- Melhora a segurança contra SQL injection
- Facilita a manutenção do banco de dados

## Autenticação e Autorização

Implementamos um sistema de autenticação usando Flask-Login para:
- Gerenciar sessões de usuário
- Proteger rotas que requerem autenticação
- Diferenciar entre usuários comuns e administradores
- Garantir a segurança das operações

### Justificativa
A segurança é fundamental em sistemas web, e o Flask-Login:
- Oferece uma solução robusta e testada
- Facilita a implementação de controle de acesso
- Segue as melhores práticas de segurança
- Integra-se bem com o Flask

## Formulários

Utilizamos Flask-WTF para:
- Criar formulários seguros
- Validar dados de entrada
- Proteger contra CSRF
- Melhorar a experiência do usuário

### Justificativa
O uso de formulários com WTForms:
- Garante a validação adequada dos dados
- Melhora a segurança da aplicação
- Reduz o código boilerplate
- Facilita a manutenção dos formulários

## Interface do Usuário

A interface foi desenvolvida com Bootstrap para:
- Criar um design responsivo
- Manter consistência visual
- Melhorar a usabilidade
- Acelerar o desenvolvimento frontend

### Justificativa
O Bootstrap foi escolhido por:
- Oferecer componentes prontos e customizáveis
- Garantir compatibilidade cross-browser
- Facilitar o desenvolvimento responsivo
- Seguir padrões modernos de design

## Funcionalidades CRUD

Implementamos CRUDs completos para todas as entidades:
- Usuários
- Categorias
- Anúncios
- Perguntas e Respostas
- Compras
- Favoritos

### Justificativa
Os CRUDs foram implementados seguindo:
- Princípios REST
- Boas práticas de UX
- Padrões de segurança
- Requisitos do sistema

## Organização do Código

O código foi organizado em:
- Módulos por funcionalidade
- Templates reutilizáveis
- Rotas bem definidas
- Componentes isolados

### Justificativa
A organização escolhida:
- Facilita a manutenção
- Melhora a legibilidade
- Permite escalabilidade
- Segue padrões de projeto

## Conclusão

O sistema foi desenvolvido seguindo as melhores práticas apresentadas nas aulas, resultando em um código:
- Bem organizado
- Seguro
- Escalável
- Fácil de manter

As escolhas técnicas foram feitas considerando:
- Requisitos do projeto
- Boas práticas de desenvolvimento
- Padrões da indústria
- Experiência do usuário
