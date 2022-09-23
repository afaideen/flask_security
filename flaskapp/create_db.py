
#Run this to create site.db
#UseSQLite Studio to view data content in db
from flaskapp import db
from run import app

with app.app_context():
    db.create_all()