#!/bin/bash
rm instance/db.sqlite
source venv/bin/activate
export FLASK_APP=scoreboard
export FLASK_DEBUG=1
python3 create_db_trueflags.py  
flask run

