from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import Player
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """
    Login page
    """
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """
    Login page for POST method
    Check if player exist (pseudo) and if password is correct
    """
    pseudo = request.form.get('pseudo')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # find player
    player = Player.query.filter_by(pseudo=pseudo).first()

    # check if the player actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # if the user doesn't exist or password is wrong, reload the page
    if not player or not check_password_hash(player.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(player, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    """
    Singin page
    """
    return render_template('signup.html')
	
@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Signin page for POST method
    Check if player does not already exist
    Check confirmation password
    """
    pseudo = request.form.get('pseudo')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    # if this returns a user, then the email already exists in database
    player = Player.query.filter_by(pseudo=pseudo).first()
    
    # if a user is found, we want to redirect back to signup page so user can try again
    if player:
        flash('Player already exists')
        return redirect(url_for('auth.signup'))

    if password1 != password2:
        flash('Password confirmation mismatch')
        return redirect(url_for('auth.signup'))

    # create a new player. Hash the password so the plaintext version isn't saved.
    new_player = Player(pseudo=pseudo, password=generate_password_hash(password1, method='sha256'), score=0)

    # add the new user to the database
    db.session.add(new_player)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    """
    Log out stuff
    """
    logout_user()
    return redirect(url_for('main.index'))