from flask_login import UserMixin
from . import db

chall_solved = db.Table('chall_solved',
                        db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
                        db.Column('chall_id', db.Integer, db.ForeignKey('chall.id')),
                        )


class Player(UserMixin, db.Model):
    """
    Player Table
    id : unique id for each player
    pseudo : name chosen by the player
    score : start with 0 and increment with successful flag submission
    challs : list of challenges validated by the player
    """
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    pseudo = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    score = db.Column(db.Integer)
    challs = db.relationship('Chall', secondary=chall_solved, backref='players')

class Chall(db.Model):
    """
    Chall Table
    id : unique if for each chall
    name : challenge name
    flag : expected flag for the challenge
    points : points given for the challenge
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    flag = db.Column(db.String(100))
    points = db.Column(db.Integer)