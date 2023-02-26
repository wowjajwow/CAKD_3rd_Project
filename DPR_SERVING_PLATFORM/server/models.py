from server import db

class Documents(db.Model):
     file_name = db.Column(db.Text, primary_key=True)
     file_dir = db.Column(db.Text, nullable=False)