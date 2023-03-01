from myPackage.__init__ import db, login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    postes = db.relationship('Postes', backref='author', lazy=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # magic method to print User
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    


# ///////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    privacy=db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # magic method to print Postes
    def __repr__(self):
        return f"Post('{self.title}')"


# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    friend_id=db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    # magic method to print Friends
    def __repr__(self):
        return f"Friend('{self.user_id}')"
    

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id =db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    resever_id=db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    friend_request_status=db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    

    # magic method to print FriendRequest
    def __repr__(self):
        return f"FriendRequest('{self.sender_id}')"