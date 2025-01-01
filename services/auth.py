from flask import request, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from models.user import User
from services.database import db
import secrets

def register(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register_user():
        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            
            print(f"Attempting to register user: email={email}, username={username}")
            
            existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
            if existing_user:
                print("Error: User already exists.")
                flash('Email or username already exists. Please choose another one.', 'danger')
                return redirect(url_for('register'))
            
            user = User(email=email, username=username)
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                print(f"User {username} registered successfully!")
                
                flash('Your account has been created successfully! You can now log in.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                print(f"Error during registration: {str(e)}")
                flash(f'Error creating account: {str(e)}', 'danger')
                return redirect(url_for('register'))
        
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            identifier = request.form['username_or_email']
            password = request.form['password']
            
            user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
            
            if user and user.check_password(password):
                random_cookie = secrets.token_hex(16)
                session['user_cookie'] = random_cookie
                
                login_user(user)
                
                flash("Logged in successfully!")
                return redirect(url_for('index'))
            
            flash("Invalid email/username or password.")
            return redirect(url_for('login'))
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user_cookie', None)
        logout_user()
        return redirect(url_for('login'))