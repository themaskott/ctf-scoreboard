# Create BDD bdd
from scoreboard import db, create_app, models

app=create_app()

challs_names = ['level{0}'.format(_) for _ in range(20)]
challs_flags = ['flag{0}'.format(_) for _ in range(20)]
challs_points = [1] * 20

with app.app_context():
    db.create_all()

    # Add challenges
    challs = [models.Chall(name=challs_names[_], flag=challs_flags[_], points=challs_points[_]) for _ in range(20)]

    db.session.add_all(challs)
    db.session.commit()