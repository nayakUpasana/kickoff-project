from db import db


class StudentProgramModel(db.Model):
    __tablename__ = 'student_program'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_names.student_id'))
    student_username = db.Column(db.String(80), db.ForeignKey('student_names.student_username'))
    program_code = db.Column(db.String(80), db.ForeignKey('academic_program.program_code'))

    student = db.relationship('StudentNameModel', foreign_keys=[student_username])
    program = db.relationship('AcademicProgramModel', foreign_keys=[program_code])

    def __init__(self, student_id, student_username, program_code):
        self.student_id = student_id
        self.student_username = student_username
        self.program_code = program_code

    def json(self):
        return {
            'student_id': self.student_id,
            'student_username': self.student_username,
            'academic_program': self.program_code
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_student_program(cls, student_username):
        return cls.query.filter_by(student_username=student_username).first()

    @classmethod
    def find_students_in_program(cls, program_code):
        return cls.query.filter_by(program_code=program_code).all()
