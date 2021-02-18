from flask_restful import Resource, reqparse
from models.academic_program import AcademicProgramModel
from models.student_program import StudentProgramModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    jwt_optional,
    get_jwt_identity
)


_prog_parser = reqparse.RequestParser()
_prog_parser.add_argument('program_code',
                          type=str,
                          required=True,
                          help="The 'program_code' field cannot be blank.")
_prog_parser.add_argument('program_name',
                          type=str,
                          required=True,
                          help="The 'program_name' field cannot be blank.")


class ProgramRegister(Resource):
    @fresh_jwt_required
    def post(self):
        data = _prog_parser.parse_args()

        if AcademicProgramModel.find_by_prog_code(data['program_code']):
            return {"message": "Program code '{}' already exists.".format(data['program_code'])}, 400

        program = AcademicProgramModel(**data)
        program.save_to_db()

        return {"message": "Program code created successfully."}, 201


class Program(Resource):
    @classmethod
    @jwt_required
    def get(cls, prog_code):
        program = AcademicProgramModel.find_by_prog_code(prog_code)
        if program:
            return program.json(), 200
        return {"message": "Program not found."}, 404

    @classmethod
    @jwt_required
    def delete(cls, prog_code):
        program = AcademicProgramModel.find_by_prog_code(prog_code)
        if not program:
            return {"message": "Program not found."}, 404

        students = StudentProgramModel.find_students_in_program(prog_code)
        if students:
            return {"message": "There are students under the program {}. Cannot be deleted.".format(prog_code)}

        program.delete_from_db()
        return {"message": "Program deleted."}, 200


class ProgramList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        programs = [prog.json() for prog in AcademicProgramModel.find_all()]
        if user_id:
            return {'Programs': programs}, 200
        return {
            'program': [program['program_code'] for program in programs],
            'message': 'More data available if you log in.'
        }, 200
