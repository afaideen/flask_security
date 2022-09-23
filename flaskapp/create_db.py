
#Run this to create site.db
#Install MySQL Workbench to view data in db
from flaskapp import db
from run import app

with app.app_context():
    db.create_all()