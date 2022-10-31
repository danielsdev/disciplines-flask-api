"""Modulo Principal do Projeto."""
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.user import Login, Register
from resources.disciplina import Disciplina, DisciplinaList
from resources.topico import Topico, TopicoList
from resources.relacionamento import Relacionamento, RelacionamentoList
import sqlalchemy.dialects.sqlite
from db import db
from ma import ma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chavesecreta'

api = Api(app)
JWTManager(app)

db.init_app(app)
ma.init_app(app)

@app.before_first_request
def criar_banco():
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    """Error Page Not Found."""
    return {"status": "Página não encontrada"}, 404

@app.errorhandler(500)
def server_error(e):
    """Error Internal Server Error."""
    return {"status": "Erro interno no servidor"}, 505

@app.errorhandler(401)
def unauthorized(e):
    """Error unauthorized."""
    return {"status": "Não autorizado"}, 401

api.add_resource(Login,
    '/login',
    '/login/'
)
api.add_resource(Register,
    '/register',
    '/register/'
)
api.add_resource(Disciplina,
    '/disciplina',
    '/disciplina/',
    '/disciplina/<int:id>',
    '/disciplina/<int:id>/',
)
api.add_resource(DisciplinaList,
    '/disciplinas',
    '/disciplinas/',
)
api.add_resource(Topico,
    '/topico',
    '/topico/',
    '/topico/<int:id>',
    '/topico/<int:id>/',
)
api.add_resource(TopicoList,
    '/topicos',
    '/topicos/',
)
api.add_resource(Relacionamento,
    '/relacionamento',
    '/relacionamento/',
    '/relacionamento/<int:id>',
    '/relacionamento/<int:id>/',
)
api.add_resource(RelacionamentoList,
    '/relacionamentos',
    '/relacionamentos/',
)
