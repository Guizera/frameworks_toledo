# Documentação de Rotas Protegidas por Login

## Visão Geral
O sistema utiliza o Flask-Login para gerenciar a autenticação e proteção das rotas. O decorator `@login_required` é usado para garantir que apenas usuários autenticados possam acessar determinadas funcionalidades.

## Rotas Públicas (Não Requerem Login)
1. **Páginas Principais**
   - `/` - Página inicial
   - `/login` - Página de login
   - `/register` - Página de registro
   - `/ads` - Listagem de anúncios
   - `/categories` - Listagem de categorias
   - `/ads/<id>` - Visualização de anúncio específico
   - `/categories/<id>` - Visualização de categoria específica

2. **Justificativa**
   - Estas rotas são públicas para permitir que visitantes:
     - Conheçam o sistema
     - Visualizem produtos disponíveis
     - Criem uma conta
     - Realizem login

## Rotas Protegidas (Requerem Login)

1. **Gerenciamento de Usuário**
   ```python
   @login_required
   - /users/<id>/edit - Edição de perfil
   - /users/<id>/delete - Exclusão de conta
   ```
   **Justificativa**: Protege informações pessoais e operações sensíveis do usuário

2. **Gerenciamento de Anúncios**
   ```python
   @login_required
   - /ads/new - Criação de anúncio
   - /ads/<id>/edit - Edição de anúncio
   - /ads/<id>/delete - Exclusão de anúncio
   - /user/ads - Lista de anúncios do usuário
   ```
   **Justificativa**: Garante que apenas usuários autenticados possam gerenciar anúncios

3. **Interações com Anúncios**
   ```python
   @login_required
   - /ads/<id>/questions - Fazer perguntas
   - /questions/<id>/answer - Responder perguntas
   - /ads/<id>/favorite - Favoritar anúncio
   - /ads/<id>/purchase - Realizar compra
   ```
   **Justificativa**: Assegura que interações sejam rastreáveis e vinculadas a usuários reais

4. **Área do Usuário**
   ```python
   @login_required
   - /user/purchases - Histórico de compras
   - /user/sales - Histórico de vendas
   - /user/favorites - Lista de favoritos
   ```
   **Justificativa**: Protege informações pessoais e transacionais do usuário

5. **Gerenciamento de Categorias (Admin)**
   ```python
   @login_required
   - /categories/new - Criação de categoria
   - /categories/<id>/edit - Edição de categoria
   - /categories/<id>/delete - Exclusão de categoria
   ```
   **Justificativa**: Restringe operações administrativas a usuários autorizados

## Implementação da Proteção

1. **Configuração do Flask-Login**
   ```python
   login_manager = LoginManager(app)
   login_manager.login_view = 'login'
   ```

2. **Proteção de Rotas**
   ```python
   @app.route('/protected_route')
   @login_required
   def protected_route():
       return 'Esta rota só é acessível após login'
   ```

3. **Verificações Adicionais**
   ```python
   if current_user.is_authenticated:
       # Lógica para usuários logados
   else:
       # Lógica para usuários não logados
   ```

## Justificativas das Implementações

1. **Segurança**
   - Proteção de dados sensíveis
   - Controle de acesso granular
   - Rastreabilidade de ações
   - Prevenção de acessos não autorizados

2. **Experiência do Usuário**
   - Fluxo claro de autenticação
   - Redirecionamento automático para login
   - Mensagens de feedback apropriadas
   - Manutenção do contexto após login

3. **Boas Práticas**
   - Uso de decorators para controle de acesso
   - Separação clara entre rotas públicas e protegidas
   - Validações em múltiplas camadas
   - Seguindo princípios de segurança web

4. **Manutenibilidade**
   - Código organizado e documentado
   - Fácil adição de novas rotas protegidas
   - Centralização da lógica de autenticação
   - Padrões consistentes de implementação
