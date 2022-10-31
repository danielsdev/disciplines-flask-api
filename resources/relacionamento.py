from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required
from models import Relacionamentos, RelacionamentosSchema, Topicos
from marshmallow.exceptions import ValidationError


class Relacionamento(Resource):

    parser = RequestParser()
    parser.add_argument("nome")
    parser.add_argument("topico1_id")
    parser.add_argument("topico2_id")

    @jwt_required
    def get(self, id=None):
        if id == None:
            return {"status": "Relacionamento inválido"}, 400
        relacionamento = Relacionamentos.query.get(id)
        if relacionamento:
            return {"relacionamento": RelacionamentosSchema().dump(relacionamento)}, 200
        else:
            return {"status": "Relacionamento não encontrado"}, 400

    @jwt_required
    def post(self):
        try:
            dados = RelacionamentosSchema().load(self.parser.parse_args())
            topico1 = Topicos.query.get(dados['topico1_id'])
            topico2 = Topicos.query.get(dados['topico2_id'])
            if topico1 and topico2:
                relacionamento = Relacionamentos(dados['nome'])
                relacionamento.topico1 = topico1
                relacionamento.topico2 = topico2
                relacionamento.persist()
                return {
                    "status": "Relacionamento cadastrado com sucesso",
                    "relacionamento": RelacionamentosSchema().dump(relacionamento)
                }, 201
            return {"status": "Tópicos inválidos"}, 400
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400

    @jwt_required
    def put(self, id=None):
        try:
            if id == None:
                return {"status": "Relacionamento inválido"}, 400
            dados = RelacionamentosSchema().load(self.parser.parse_args())
            relacionamento = Relacionamentos.query.get(id)
            topico1 = Topicos.query.get(dados['topico1_id'])
            topico2 = Topicos.query.get(dados['topico2_id'])
            if topico1 and topico2:
                relacionamento.nome = dados['nome']
                relacionamento.topico1 = topico1
                relacionamento.topico2 = topico2
                relacionamento.persist()
                return {
                    "status": "Relacionamento atualizado com sucesso",
                    "relacionamento": RelacionamentosSchema().dump(relacionamento)
                }, 200
            return {"status": "Tópicos inválidos"}, 400
        except ValidationError as m_error:
            return m_error.normalized_messages(), 400

    @jwt_required
    def delete(self, id=None):
        if id == None:
            return {"status": "Relacionamento inválido"}, 400
        relacionamento = Relacionamentos.query.get(id)
        if relacionamento:
            relacionamento.delete()
            return {"status": "Relacionamento deletado com sucesso"}
        return {"status": "Relacionamento não encontrado!"}, 400

class RelacionamentoList(Resource):

    @jwt_required
    def get(self):
        return {
            "relacionamentos": RelacionamentosSchema(many=True).dump(Relacionamentos.query.all())
        }
