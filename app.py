from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Formulários
class UserForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

# Rotas básicabasicas
@app.route('/')
def home():
    latest_ads = Ad.query.order_by(Ad.created_at.desc()).limit(6).all()
    return render_template('home.html', latest_ads=latest_ads)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class CategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Descrição', validators=[Length(max=200)])
    submit = SubmitField('Salvar')

class AdForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    price = FloatField('Preço', validators=[DataRequired()])
    category_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

class QuestionForm(FlaskForm):
    text = TextAreaField('Pergunta', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Enviar Pergunta')

class AnswerForm(FlaskForm):
    text = TextAreaField('Resposta', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Enviar Resposta')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page if next_page else url_for('home'))
        flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email já cadastrado. Por favor, use outro email.', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/<int:id>')
@login_required
def view_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/view.html', user=user)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if user != current_user and not current_user.is_admin:
        flash('Você não tem permissão para editar este usuário.', 'danger')
        return redirect(url_for('list_users'))
    
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('view_user', id=user.id))
    return render_template('users/edit.html', form=form, user=user)

@app.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user != current_user and not current_user.is_admin:
        flash('Você não tem permissão para excluir este usuário.', 'danger')
        return redirect(url_for('list_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('list_users'))

# Rotas para Anúncios
@app.route('/ads')
def list_ads():
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    
    query = Ad.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Ad.title.ilike(f'%{search}%'))
    
    ads = query.order_by(Ad.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('ads/list.html', ads=ads, categories=categories, 
                         current_category_id=category_id, search=search)

@app.route('/ads/new', methods=['GET', 'POST'])
@login_required
def create_ad():
    form = AdForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        ad = Ad(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        db.session.add(ad)
        db.session.commit()
        flash('Anúncio criado com sucesso!', 'success')
        return redirect(url_for('view_ad', id=ad.id))
    return render_template('ads/form.html', form=form, title='Novo Anúncio')

@app.route('/ads/<int:id>')
def view_ad(id):
    ad = Ad.query.get_or_404(id)
    question_form = QuestionForm()
    answer_form = AnswerForm()
    return render_template('ads/view.html', ad=ad, question_form=question_form, answer_form=answer_form)

@app.route('/ads/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ad(id):
    ad = Ad.query.get_or_404(id)
    if ad.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para editar este anúncio.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    form = AdForm(obj=ad)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        ad.title = form.title.data
        ad.description = form.description.data
        ad.price = form.price.data
        ad.category_id = form.category_id.data
        db.session.commit()
        flash('Anúncio atualizado com sucesso!', 'success')
        return redirect(url_for('view_ad', id=ad.id))
    return render_template('ads/form.html', form=form, title='Editar Anúncio')

@app.route('/ads/<int:id>/delete', methods=['POST'])
@login_required
def delete_ad(id):
    ad = Ad.query.get_or_404(id)
    if ad.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para excluir este anúncio.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    db.session.delete(ad)
    db.session.commit()
    flash('Anúncio excluído com sucesso!', 'success')
    return redirect(url_for('list_ads'))

@app.route('/user/ads')
@login_required
def user_ads():
    ads = Ad.query.filter_by(user_id=current_user.id).order_by(Ad.created_at.desc()).all()
    return render_template('ads/user_ads.html', ads=ads)

# Rotas para Perguntas e Respostas
@app.route('/ads/<int:ad_id>/questions', methods=['POST'])
@login_required
def create_question(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        question = Question(
            text=form.text.data,
            user_id=current_user.id,
            ad_id=ad.id
        )
        db.session.add(question)
        db.session.commit()
        flash('Pergunta enviada com sucesso!', 'success')
    return redirect(url_for('view_ad', id=ad.id))

@app.route('/questions/<int:id>/answer', methods=['POST'])
@login_required
def create_answer(id):
    question = Question.query.get_or_404(id)
    ad = question.ad
    
    if ad.user_id != current_user.id:
        flash('Apenas o vendedor pode responder perguntas.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(
            text=form.text.data,
            question_id=question.id
        )
        db.session.add(answer)
        db.session.commit()
        flash('Resposta enviada com sucesso!', 'success')
    return redirect(url_for('view_ad', id=ad.id))

@app.route('/questions/<int:id>/delete', methods=['POST'])
@login_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    ad = question.ad
    
    if question.user_id != current_user.id and ad.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta pergunta.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    db.session.delete(question)
    db.session.commit()
    flash('Pergunta excluída com sucesso!', 'success')
    return redirect(url_for('view_ad', id=ad.id))

@app.route('/answers/<int:id>/delete', methods=['POST'])
@login_required
def delete_answer(id):
    answer = Answer.query.get_or_404(id)
    ad = answer.question.ad
    
    if ad.user_id != current_user.id:
        flash('Apenas o vendedor pode excluir respostas.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    db.session.delete(answer)
    db.session.commit()
    flash('Resposta excluída com sucesso!', 'success')
    return redirect(url_for('view_ad', id=ad.id))



@app.route('/user/sales')
@login_required
def user_sales():
    ads = Ad.query.filter_by(user_id=current_user.id).all()
    ad_ids = [ad.id for ad in ads]
    sales = Purchase.query.filter(Purchase.ad_id.in_(ad_ids)).order_by(Purchase.created_at.desc()).all()
    return render_template('purchases/sales.html', sales=sales)

@app.route('/user/purchases')
@login_required
def user_purchases():
    purchases = Purchase.query.filter_by(user_id=current_user.id).order_by(Purchase.created_at.desc()).all()
    return render_template('purchases/list.html', purchases=purchases)

@app.route('/ads/<int:ad_id>/purchase', methods=['POST'])
@login_required
def create_purchase(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    
    if ad.user_id == current_user.id:
        flash('Você não pode comprar seu próprio anúncio.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    if Purchase.query.filter_by(ad_id=ad.id).first():
        flash('Este item já foi vendido.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    purchase = Purchase(
        user_id=current_user.id,
        ad_id=ad.id,
        total_value=ad.price
    )
    db.session.add(purchase)
    db.session.commit()
    
    flash('Compra realizada com sucesso!', 'success')
    return redirect(url_for('user_purchases'))

@app.route('/purchases/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_purchase(id):
    purchase = Purchase.query.get_or_404(id)
    
    if purchase.user_id != current_user.id and purchase.ad.user_id != current_user.id:
        flash('Você não tem permissão para cancelar esta compra.', 'danger')
        return redirect(url_for('user_purchases'))
    
    db.session.delete(purchase)
    db.session.commit()
    flash('Compra cancelada com sucesso!', 'success')
    
    if purchase.user_id == current_user.id:
        return redirect(url_for('user_purchases'))
    return redirect(url_for('user_sales'))

@app.route('/user/favorites')
@login_required
def user_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.created_at.desc()).all()
    return render_template('favorites/list.html', favorites=favorites)

@app.route('/ads/<int:ad_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    
    if ad.user_id == current_user.id:
        flash('Você não pode favoritar seu próprio anúncio.', 'danger')
        return redirect(url_for('view_ad', id=ad.id))
    
    favorite = Favorite.query.filter_by(user_id=current_user.id, ad_id=ad.id).first()
    
    if favorite:
        db.session.delete(favorite)
        message = 'Anúncio removido dos favoritos.'
    else:
        favorite = Favorite(user_id=current_user.id, ad_id=ad.id)
        db.session.add(favorite)
        message = 'Anúncio adicionado aos favoritos!'
    
    db.session.commit()
    flash(message, 'success')
    
    if request.args.get('redirect') == 'favorites':
        return redirect(url_for('user_favorites'))
    return redirect(url_for('view_ad', id=ad.id))

# Rotas para Categorias
@app.route('/categories')
def list_categories():
    categories = Category.query.all()
    return render_template('categories/list.html', categories=categories)

@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def create_category():
    if not current_user.is_admin:
        flash('Apenas administradores podem criar categorias.', 'danger')
        return redirect(url_for('list_categories'))
    
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('list_categories'))
    return render_template('categories/form.html', form=form, title='Nova Categoria')

@app.route('/categories/<int:id>')
def view_category(id):
    category = Category.query.get_or_404(id)
    ads = Ad.query.filter_by(category_id=id).order_by(Ad.created_at.desc()).all()
    return render_template('categories/view.html', category=category, ads=ads)

@app.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    if not current_user.is_admin:
        flash('Apenas administradores podem editar categorias.', 'danger')
        return redirect(url_for('list_categories'))
    
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('view_category', id=category.id))
    return render_template('categories/form.html', form=form, title='Editar Categoria')

@app.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    if not current_user.is_admin:
        flash('Apenas administradores podem excluir categorias.', 'danger')
        return redirect(url_for('list_categories'))
    
    category = Category.query.get_or_404(id)
    if category.ads:
        flash('Não é possível excluir uma categoria que possui anúncios.', 'danger')
        return redirect(url_for('list_categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('list_categories'))

if __name__ == '__main__':
    app.run(debug=True) 