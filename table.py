from config import db, app
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wxId = db.Column(db.String(30), unique=True, nullable=False, default="")
    Interests = db.Column(db.Integer, unique=False, nullable=False, default=0)
    MarkNum = db.Column(db.Integer, unique=False, nullable=False, default=0)
    def __init__(self, wxId, Interests, MarkNum):
        self.wxId = wxId
        self.Interests = Interests
        self.MarkNum = MarkNum

    def __repr__(self):
        return '<User %r>' % self.wxId

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Lecture(UserMixin, db.Model):
    __tablename__ = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    Subject = db.Column(db.String(20), unique=False, nullable=False, default="")
    Title = db.Column(db.String(50), unique=False, nullable=False, default="")
    Lecturer = db.Column(db.String(100), unique=False, nullable=False, default="")
    Year = db.Column(db.Integer, unique=False, nullable=False, default=0)
    Month = db.Column(db.Integer, unique=False, nullable=False, default=0)
    Day = db.Column(db.Integer, unique=False, nullable=False, default=0)
    Location = db.Column(db.String(50), unique=False, nullable=False, default="")
    Content = db.Column(db.String(5000), unique=False, nullable=True, default="")
    def __init__(self, Subject, Title, Lecturer, Year, Month, Day, Location, Content):
        self.Subject = Subject
        self.Title = Title
        self.Lecturer = Lecturer
        self.Year = Year
        self.Month = Month
        self.Day = Day
        self.Location = Location
        self.Content = Content

    def __repr__(self):
        return '<Lecture %r>' % self.Title

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

# 收藏关系
class userToLec(UserMixin,db.Model):
    __tablename__ = 'UserToLec'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=False, nullable=False, default=0)
    LecId = db.Column(db.Integer, unique=False, nullable=False,default=0)

    def __repr__(self):
        return '<userToLec %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
