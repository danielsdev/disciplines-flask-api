from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_restful.reqparse import RequestParser
from marshmallow.exceptions import ValidationError
from models import UsuariosSchema, Usuarios
from sqlalchemy.exc import IntegrityError
import datetime

class Login(Resource):
    """."""

    parser = RequestParser()
    parser.add_argument("email")
    parser.add_argument("senha")

    def post(self):
        """."""
        try:
            dados = UsuariosSchema().load(self.parser.parse_args())
            usuario = Usuarios.query.filter_by(email=dados['email']).first()
            if usuario and usuario.verificar_senha(dados['senha']):
                time = datetime.timedelta(days=1)
                return {"JWT": create_access_token(usuario.id, expires_delta=time)}
            return {"status": 'Usuario não Existe ou Senha Incorreta!'}
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400


class Register(Resource):
    """."""

    parser = RequestParser()
    parser.add_argument("email")
    parser.add_argument("senha")
    parser.add_argument("level", default=1)

    def post(self):
        """."""
        try:
            dados = UsuariosSchema().load(self.parser.parse_args())
            usuario = Usuarios(**dados)
            usuario.hash_senha()
            try:
                usuario.persist()
                return {'status': 'Usuario Cadastrado com Sucesso!', 'id': usuario.id}, 201
            except IntegrityError:
                return {"status": "Email já Cadastrado!"}, 400
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400
