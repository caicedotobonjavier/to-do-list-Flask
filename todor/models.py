from todor import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # The `username` attribute in the `User` class is defining a column in the database table for the
    # `User` model. It is of type `String` with a maximum length of 20 characters, set to be unique
    # (no two users can have the same username) and cannot be null (required field).
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def __repr__(self):
        return self.username


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=False)

    def __init__(self, user, title, description, status=False):
        self.user = user
        self.title = title
        self.description = description
        self.status = status
    

    def __repr__(self):
        return self.title


