from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def __init__(user, real_pas, given_pas):
        password = set_password (real_pas)
        username = user

    # is_active() and is_anonymous() stay the same as in the parent class

    def get_id(self):
        """Return the username to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def __repr__(self):
        return '<User {}>'.format(self.username)
