from sqlalchemy import Unicode
from app import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique = True)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return "<User %r>" % self.username


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", foreign_keys = user_id)

    def __init__(self, user_id, date, content):
        self.user_id = user_id
        self.date = date
        self.content = content

    def __repr__(self):
        return "<Post %r>" % self.content

class Record(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    user_name = db.Column(db.Integer, db.ForeignKey("user.name"))
    service_content = db.Column(db.Integer, db.ForeignKey("service.content"))

    user = db.relationship("User", foreign_keys = user_name)
    service = db.relationship("Service", foreign_keys = service_content)

    def __init__(self, date ,user_name, service_content):
        self.date = date
        self.user_name = user_name
        self.service_content = service_content

    def __repr__(self):
        return "Record %r" % self.id