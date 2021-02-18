from flask_restful import Resource, reqparse
from models.student_program import StudentProgramModel
from models.student_names import StudentNameModel
from models.academic_program import AcademicProgramModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required
)

_stu_prog_parser = reqparse.RequestParser()
_stu_prog_parser.add_argument('student_username',
                              type=str,
                              required=True,
                              help="The Student Username field cannot be blank.")
_stu_prog_parser.add_argument('program_code',
                              type=str,
                              required=True,
                              help="Please enter a valid Program Code.")


class StudentProgRegister(Resource):
    @fresh_jwt_required
    def post(self):
        data = _stu_prog_parser.parse_args()

        if not StudentNameModel.find_by_student_username(data['student_username']):
            return {"message": "The student by the username '{}' "
                               "is not available.".format(data['student_username'])}, 404

        stu_info = StudentNameModel.find_by_student_username(data['student_username'])
        stu_id = stu_info.student_id

        if not AcademicProgramModel.find_by_prog_code(data['program_code']):
            return {"message": "{} is not a valid program code.".format(data['program_code'])}, 404

        stu_prog = StudentProgramModel(stu_id, **data)
        stu_prog.save_to_db()

        return {"message": "Student program added successfully."}, 201


class StudentProgram(Resource):
    @classmethod
    @jwt_required
    def get(cls, student_username):
        student = StudentProgramModel.find_student_program(student_username)
        if student:
            return student.json(), 200
        return {"message": "Student not found."}, 404

    @classmethod
    @jwt_required
    def delete(cls, student_username):
        student = StudentProgramModel.find_student_program(student_username)
        if not student:
            return {"message": "Student not found."}, 404
        student.delete_from_db()
        return {"message": "Student program deleted successfully."}, 200


class StudentInProgram(Resource):
    @classmethod
    @jwt_required
    def get(cls, program_code):

        program = AcademicProgramModel.find_by_prog_code(program_code)
        if not program:
            return {"message": "Program '{}' not found.".format(program_code)}

        students = [student.json() for student in StudentProgramModel.find_students_in_program(program_code)]
        if students:
            return {'students': [student['student_username'] for student in students]}, 200

        return {"message": "No students under the program '{}'.".format(program_code)}, 404
