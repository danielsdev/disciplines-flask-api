"""Modelos do Sistema."""
from flask_marshmallow.fields import fields
from passlib.hash import pbkdf2_sha256
from db import db
from ma import ma

class Disciplinas(db.Model):

    __tablename__ = "disciplinas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    topicos = db.relationship('Topicos', backref='disciplina', lazy=True)

    def __init__(self, nome=None, curso=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome = nome
        self.curso = curso

    def persist(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Disciplina %r>' % self.nome


class Topicos(db.Model):

    __tablename__ = "topicos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    disciplina_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'disciplinas.id',
            onupdate="CASCADE",
            ondelete="SET NULL"
        ),
        nullable=False
    )

    def __init__(self, nome=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome = nome

    def persist(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Topico %r>' % self.nome


class Relacionamentos(db.Model):

    __tablename__ = 'relacionamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    topico1_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'topicos.id',
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    topico2_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'topicos.id',
            onupdate="CASCADE",
            ondelete="SET NULL"
        )
    )
    topico1 = db.relationship(
        "Topicos",
        primaryjoin=Topicos.id == topico1_id,
    )
    topico2 = db.relationship(
        "Topicos",
        primaryjoin=Topicos.id == topico2_id,
    )

    def __init__(self, nome=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome = nome

    def persist(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Relacionamento %r>' % self.nome


class Usuarios(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    level = db.Column(db.Integer, nullable=False, default="1")

    def __init__(self, email=None, senha=None, level=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = email
        self.senha = senha
        self.level = level

    def hash_senha(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

    def verificar_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)

    def persist(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.email


class UsuariosSchema(ma.Schema):

    class Meta:
        model = Usuarios

    email = fields.Str(required=True)
    senha = fields.Str(required=True)
    level = fields.Integer(load_only=True)


class DisciplinasSchema(ma.Schema):

    class Meta:

        model = Disciplinas

    id = fields.Integer(dump_only=True)
    nome = fields.Str(required=True)
    curso = fields.Str(required=True)


class TopicosSchema(ma.Schema):

    class Meta:

        model = Topicos

    id = fields.Integer(dump_only=True)
    nome = fields.Str(required=True)
    disciplina_id = fields.Integer(required=True, load_only=True)
    disciplina = fields.Nested(DisciplinasSchema, allow_none=True)


class RelacionamentosSchema(ma.Schema):

    class Meta:

        model = Relacionamentos

    id = fields.Integer(dump_only=True)
    nome = fields.Str(required=True)
    topico1_id = fields.Integer(required=True, load_only=True)
    topico2_id = fields.Integer(required=True, load_only=True)
    topico1 = fields.Nested(TopicosSchema, allow_none=True, dump_only=True)
    topico2 = fields.Nested(TopicosSchema, allow_none=True, dump_only=True)
