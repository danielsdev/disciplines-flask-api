from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Usuarios, Topicos, TopicosSchema, Disciplinas
from marshmallow.exceptions import ValidationError


def verifyLevel():
    user = Usuarios.query.get(get_jwt_identity())
    if user and user.level != 1:
        abort(403, status="Você não possui a permissão necessária")


class Topico(Resource):
    
    parser = RequestParser()
    parser.add_argument("nome")
    parser.add_argument("disciplina_id")

    @jwt_required
    def get(self, id=None):
        if id == None:
            return {"status": "tópico inválido"}, 400
        topico = Topicos.query.get(id)
        if topico:
            return {"topico": TopicosSchema().dump(topico)}, 200
        else:
            return {"status": "tópico não encontrado"}, 400

    @jwt_required
    def post(self):
        try:
            verifyLevel()
            dados = TopicosSchema().load(self.parser.parse_args())
            disciplina = Disciplinas.query.get(dados['disciplina_id'])
            if disciplina:
                topico = Topicos(**dados)
                topico.disciplina = disciplina
                topico.persist()
                return {
                    "status": "Tópico cadastrado com sucesso",
                    "topico": TopicosSchema().dump(topico)
                }, 201
            return {"status": "Disciplina não encontrada"}, 400
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400

    @jwt_required
    def put(self, id=None):
        try:
            verifyLevel()
            if id == None:
                return {"status": "Tópico inválido"}, 400
            dados = TopicosSchema().load(self.parser.parse_args())
            topico = Topicos.query.get(id)
            if topico:
                topico.nome = dados['nome']
                if topico.disciplina_id != dados['disciplina_id']:
                    disciplina = Disciplinas.query.get(dados['disciplina_id'])
                    topico.disciplina = disciplina
                topico.persist()
                return {
                    "status": "Tópico atualizado com sucesso",
                    "topico": TopicosSchema().dump(topico)
                }, 200
            return {"status": "Tópico não encontrado"}, 400
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400

    @jwt_required
    def delete(self, id=None):
        verifyLevel()
        if id == None:
            return {"status": "Tópico invalido"}, 400
        topico = Topicos.query.get(id)
        if topico:
            topico.delete()
            return {
                "status": "Tópico deletado com sucesso"
            }
        return {"status": "Tópico não encontrado"}, 400

class TopicoList(Resource):

    @jwt_required
    def get(self):
        return {"topicos": TopicosSchema(many=True).dump(Topicos.query.all())}
