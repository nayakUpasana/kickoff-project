from db import db


class TransferCourseModel(db.Model):
    __tablename__ = 'transfer_course'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_names.student_id'))
    student_username = db.Column(db.String(80), db.ForeignKey('student_names.student_username'))
    course = db.Column(db.String(20))
    course_status = db.Column(db.String(50))

    student = db.relationship('StudentNameModel', foreign_keys=[student_username])

    def __init__(self, student_id, student_username, course, course_status):
        self.student_id = student_id
        self.student_username = student_username
        self.course = course
        self.course_status = course_status

    def json(self):
        return {
            'student_id': self.student_id,
            'student_username': self.student_username,
            'course': self.course,
            'course_status': self.course_status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_student_username(cls, student_username):
        return cls.query.filter_by(student_username=student_username).first()

