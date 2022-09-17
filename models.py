from flask_sqlalchemy import SQLALCHEMY
from flask_bcrypt import flask_bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):
    """users on site"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20)
        nullable = False,
        unique = True,
        primary_key = True,
    )
    password = db.Column(
        db.String(50),
        nullable = False
    )
    email = db.Column(
        db.String(50),
        nullable = False
    )
    first_name = db.Column(
        db.String(50),
        nullable = False
    )
    last_name = db.Column(
        db.String(50),
        nullable = False
    )
    is_admin = db.Column(
        db.Boolean,
        nullable = False,
        default = False
    )

    feedback = db.relationship("Feedback", backref = "user", cascade= "all,delete")

    #class methods

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """User registration and hashing of password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            email = email
        )

    @classmethod
    def authenticate(cls, username, password):
        """Checks that user is in database and hashed password matches
        
        Return user if validl else return False"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "feedback"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    title = db.Column(
        db.String(100),
        nullable = False
    )
    content = db.Column(
        db.Text,
        nullable = False
    )
    username = db.Column(
        db.String(20),
        db.ForeignKey('user.username'),
        nullable = False
    )


    