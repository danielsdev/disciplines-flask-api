from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Disciplinas, DisciplinasSchema, Usuarios
from marshmallow.exceptions import ValidationError

def verifyLevel():
    user = Usuarios.query.get(get_jwt_identity())
    if user and user.level != 1:
        abort(403, status="Você não possui a permissão necessária")


class Disciplina(Resource):

    parser = RequestParser()
    parser.add_argument("nome")
    parser.add_argument("curso")

    @jwt_required
    def get(self, id=None):
        if id == None:
            return {"status": "Disciplina inválida"}, 400
        disciplina = Disciplinas.query.get(id)
        if disciplina:
            return {'disciplina': DisciplinasSchema().dump(disciplina)}, 200
        else:
            return {"status": "disciplina não encontrada!"}, 400


    @jwt_required
    def post(self):
        try:
            verifyLevel()
            dados = DisciplinasSchema().load(self.parser.parse_args())
            disciplina = Disciplinas(**dados)
            disciplina.persist()
            return {"disciplina": DisciplinasSchema().dump(disciplina)}, 201
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400

    @jwt_required
    def put(self, id=None):
        try:
            verifyLevel()
            if id == None:
                return {"status": "disciplina invalida!"}, 400
            dados = DisciplinasSchema().load(self.parser.parse_args())
            disciplina = Disciplinas.query.get(id)
            if disciplina:
                disciplina.nome = dados['nome']
                disciplina.curso = dados['curso']
                disciplina.persist()
                return {
                    "status": "Disciplina atualizada com sucesso",
                    "disciplina": DisciplinasSchema().dump(disciplina)
                }
            return {"status": "Disciplina não encontrada"}, 400
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400

    @jwt_required
    def delete(self, id=None):
        verifyLevel()
        if id == None:
            return {"status": "Disciplina inválida"}, 400
        disciplina = Disciplinas.query.get(id)
        if disciplina:
            disciplina.delete()
            return {"status": "Disciplina deletada com sucesso"}
        return {"status": "Disciplina não encontrada"}


class DisciplinaList(Resource):

    @jwt_required
    def get(self):
        return {'disciplinas': DisciplinasSchema(many=True).dump(Disciplinas.query.all())}
