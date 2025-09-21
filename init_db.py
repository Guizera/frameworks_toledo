from app import app, db
from models import User, Category
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Criar categorias iniciais
        categorias = [
            Category(name='Eletrônicos', description='Smartphones, tablets, computadores e acessórios'),
            Category(name='Móveis', description='Móveis para casa e escritório'),
            Category(name='Roupas', description='Vestuário masculino e feminino'),
            Category(name='Livros', description='Livros novos e usados'),
            Category(name='Esportes', description='Equipamentos e acessórios esportivos'),
            Category(name='Casa', description='Utensílios e decoração para casa'),
            Category(name='Jogos', description='Videogames e jogos'),
            Category(name='Automóveis', description='Carros, motos e acessórios')
        ]
        
        # Adicionar categorias
        for categoria in categorias:
            existing = Category.query.filter_by(name=categoria.name).first()
            if not existing:
                db.session.add(categoria)
        
        # Criar usuário admin
        admin = User.query.filter_by(email='admin@admin.com').first()
        if not admin:
            admin = User(
                name='Administrador',
                email='admin@admin.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
        
        db.session.commit()
        print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_db()
