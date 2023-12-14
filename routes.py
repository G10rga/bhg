from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user

from forms import RegistrationForm, LoginForm
from extensions import app, db, bcrypt
from models import User

# Sample data for items (you can replace this with your actual data)
items = [
    {'id': 1, 'name': 'Item 1', 'price': 10.99, 'image': 'item1.jpg'},
    {'id': 2, 'name': 'Item 2', 'price': 19.99, 'image': 'item2.jpg'},
    {'id': 3, 'name': 'Item 2', 'price': 19.99, 'image': 'PC1.png'}
]

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/Pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/')
def index():
    return render_template('index.html', items=items)  # Pass the items to the template

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/store')
def store():
    return render_template('store.html', items=items)  # Pass the items to the template

@app.route('/configurator')
def configurator():
    return render_template('configurator.html')

@app.route('/store/<int:item_id>')
def item_detail(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    return render_template('item_detail.html', item=item)
