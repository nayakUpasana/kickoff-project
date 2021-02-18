from db import db


class AcademicProgramModel(db.Model):
    __tablename__ = 'academic_program'
    __table_args__ = {'extend_existing': True}

    program_id = db.Column(db.Integer, primary_key=True)
    program_code = db.Column(db.String(80), unique=True)
    program_name = db.Column(db.String(80))

    def __init__(self, program_code, program_name):
        self.program_code = program_code
        self.program_name = program_name

    def json(self):
        return {
            'program_code': self.program_code,
            'program_name': self.program_name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_prog_code(cls, program_code):
        return cls.query.filter_by(program_code=program_code).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
