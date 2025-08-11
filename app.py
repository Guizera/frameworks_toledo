from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Rotas básicas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/user/ads')
@login_required
def user_ads():
    return render_template('user_ads.html')

@app.route('/user/purchases')
@login_required
def user_purchases():
    return render_template('user_purchases.html')

@app.route('/user/sales')
@login_required
def user_sales():
    return render_template('user_sales.html')

@app.route('/user/favorites')
@login_required
def user_favorites():
    return render_template('user_favorites.html')

if __name__ == '__main__':
    app.run(debug=True) 