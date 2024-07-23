import bcrypt
from flask_sqlalchemy import SQLAlchemy
#from argon2 import PasswordHasher
#from argon2.exceptions import VerifyMismatchError
from . import db
from datetime import datetime
import bcrypt


#ph = PasswordHasher()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        #self.password_hash = ph.hash(password)
        salt = bcrypt.gensalt()  # Génère un nouveau sel
        self.password_hash =  bcrypt.hashpw(password.encode('utf-8'), salt)


    def check_password(self, password):
        # Ensure the stored password hash is in bytes
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
