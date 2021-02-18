from flask_restful import Resource, reqparse
from models.student_names import StudentNameModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required
)

_student_parser = reqparse.RequestParser()
_student_parser.add_argument('student_username',
                             type=str,
                             required=True,
                             help="The 'student_username' field cannot be blank.")
_student_parser.add_argument('first_name',
                             type=str,
                             required=True,
                             help="The 'first_name' field cannot be blank.")
_student_parser.add_argument('last_name',
                             type=str,
                             required=False)


class StudentNameRegister(Resource):
    @fresh_jwt_required
    def post(self):
        data = _student_parser.parse_args()

        if StudentNameModel.find_by_student_username(data['student_username']):
            return {"message": "A student with the username '{}'"
                               " already exists.".format(data['student_username'])}, 400

        student = StudentNameModel(**data)
        student.save_to_db()

        return {"message": "Student record created successfully."}, 201


class StudentName(Resource):

    @classmethod
    @jwt_required
    def get(cls, student_id):
        student = StudentNameModel.find_by_student_id(student_id)
        if not student:
            return {"message": "Student not found with ID: {}.".format(student_id)}, 404
        return student.json()

    @classmethod
    @jwt_required
    def delete(cls, student_id):
        student = StudentNameModel.find_by_student_id(student_id)
        if not student:
            return {"message": "Student not found with ID: {}.".format(student_id)}, 404
        student.delete_from_db()
        return {"message": "Student with ID: {} was successfully deleted.".format(student_id)}, 201
