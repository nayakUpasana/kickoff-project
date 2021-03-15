from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.student_names import StudentNameRegister, StudentName
from resources.academic_program import ProgramRegister, Program, ProgramList
from resources.student_program import StudentProgRegister, StudentProgram, StudentInProgram
from resources.transfer_courses import TransferCourseRegister, TransferCourse

from db import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/my_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'moon'
api = Api(app)

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(UserRegister, '/user_register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(StudentNameRegister, '/student_name_register')
api.add_resource(StudentName, '/student_name/<int:student_id>')
api.add_resource(ProgramRegister, '/program_register')
api.add_resource(Program, '/program/<string:prog_code>')
api.add_resource(ProgramList, '/programs')
api.add_resource(StudentProgRegister, '/student_prog_register')
api.add_resource(StudentProgram, '/student_program/<string:student_username>')
api.add_resource(StudentInProgram, '/student_in_program/<string:program_code>')
api.add_resource(TransferCourseRegister, '/transfer_course_register')
api.add_resource(TransferCourse, '/transfer_course/<string:student_username>')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
