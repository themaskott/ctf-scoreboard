from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Chall, Player
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Index page
    """
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    """
    View current player profile
    For logged current player
    """
    return render_template('profile.html', player=current_user)


@main.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """
    Submit flags for challenges
    For logged player
    """
    if request.method == 'GET':
        challs = Chall.query.all()
        return render_template('submit.html', challs=challs)

    if request.method == 'POST':
        chall_name = request.form.get('chall')
        submited_flag = request.form.get('flag')
        chall = Chall.query.filter_by(name=chall_name).first()
        correct_flag = chall.flag

        # Flag is correct and current player have not already validate it
        if correct_flag == submited_flag and not chall in current_user.challs:
            current_user.challs.append(chall)
            current_user.score += chall.points
            db.session.commit()
            flash('Correct', category='info')
            return redirect(url_for('main.submit'))
        
        # Current player have already validate this challenge
        elif correct_flag == submited_flag and chall in current_user.challs:
            flash('Challenge already validated', category='error')
            return redirect(url_for('main.submit'))
        
        # Flag is not correct
        else:
            flash('Wrong flag', category='error')
            return redirect(url_for('main.submit'))

@main.route('/scoreboard')
@login_required
def scoreboard():
    """
    View score board
    """
    challs = Chall.query.all()
    players = Player.query.all()

    # Sort players by scores
    players.sort(key=lambda x: x.score, reverse=True)    
    return render_template('scoreboard.html', challs=challs, players=players)

