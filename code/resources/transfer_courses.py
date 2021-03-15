from flask_restful import Resource, reqparse
from models.transfer_courses import TransferCourseModel
from models.student_names import StudentNameModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required
)

_transfer_parse = reqparse.RequestParser()
_transfer_parse.add_argument('student_username',
                              type=str,
                              required=True,
                              help="The Student Username field cannot be blank.")
_transfer_parse.add_argument('course',
                              type=str,
                              required=True,
                              help="The Course field cannot be blank.")
_transfer_parse.add_argument('course_status',
                              type=str,
                              required=True,
                              choices=('Completed', 'Currently Enrolled', 'Planning'),
                              help="The Course Status field cannot be blank and needs to have a "
                                   "value either 'Completed', 'Currently Enrolled' or 'Planning'.")


class TransferCourseRegister(Resource):
    @fresh_jwt_required
    def post(self):
        data = _transfer_parse.parse_args()

        if not StudentNameModel.find_by_student_username(data['student_username']):
            return {"message": "The student by username '{}' is not available.".format(data['student_username'])}, 404

        stu_info = StudentNameModel.find_by_student_username(data['student_username'])
        stu_id = stu_info.student_id

        transfer_course = TransferCourseModel(stu_id, **data)
        transfer_course.save_to_db()

        return {"message": "Transfer course added successfully."}, 201


class TransferCourse(Resource):
    @classmethod
    @jwt_required
    def get(cls, student_username):
        student = TransferCourseModel.find_by_student_username(student_username)
        if student:
            return student.json(), 200
        return {"message": "Student not found."}, 404

    @classmethod
    @jwt_required
    def delete(cls, student_username):
        student = TransferCourseModel.find_by_student_username(student_username)
        if not student:
            return {"message": "Student not found."}, 404
        student.delete_from_db()
        return {"message": "Transfer course deleted successfully."}, 200


