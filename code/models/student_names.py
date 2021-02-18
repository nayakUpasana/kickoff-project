from db import db


class StudentNameModel(db.Model):
    __tablename__ = 'student_names'
    __table_args__ = {'extend_existing': True}

    student_id = db.Column(db.Integer, primary_key=True)
    student_username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def __init__(self, student_username, first_name, last_name):
        self.student_username = student_username
        self.first_name = first_name
        self.last_name = last_name

    def json(self):
        return {
            'student_id': self.student_id,
            'student_username': self.student_username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first()

    @classmethod
    def find_by_student_username(cls, student_username):
        return cls.query.filter_by(student_username=student_username).first()
