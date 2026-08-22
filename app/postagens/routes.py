from flask_jwt_extended import current_user, jwt_required
from flask_smorest import abort
from sqlalchemy import select

from app import db
from app.auth.models import Role
from app.moderacao.services import moderar_postagem
from app.postagens import postagens_bp
from app.postagens.models import Estado, Postagem, Visibilidade
from app.postagens.schemas import (
    PostagemPostSchema,
    PostagemQuerySchema,
    PostagemSchema,
)


@postagens_bp.route('/me')
@postagens_bp.arguments(PostagemQuerySchema, location='query')
@postagens_bp.response(200, PostagemSchema(many=True, exclude=['autor']))
@jwt_required()
def minhas_postagens(query):
    estado = query.get('estado')
    visibilidade = query.get('visibilidade')

    stmt = select(Postagem).where(
        Postagem.autor == current_user
    )

    if estado:
        stmt = stmt.where(
            Postagem.estado == estado
        )

    if visibilidade:
        stmt = stmt.where(
            Postagem.visibilidade == visibilidade
        )

    return db.session.scalars(stmt).all()


@postagens_bp.route('/<int:postagem_id>')
@postagens_bp.response(200, PostagemSchema(exclude=['autor']))
@jwt_required()
def detail_postagem(postagem_id):
    postagem = db.session.scalar(
        select(Postagem).where(
            Postagem.autor == current_user,
            Postagem.id == postagem_id
        )
    )

    if not postagem:
        return abort(404)

    return postagem


@postagens_bp.route('/<int:postagem_id>', methods=['PUT'])
@postagens_bp.arguments(schema=PostagemPostSchema)
@postagens_bp.response(200, PostagemSchema(exclude=['autor']))
@jwt_required()
def atualizar_postagem(data, postagem_id):
    postagem = db.session.scalar(
        select(Postagem).where(
            Postagem.id == postagem_id,
            Postagem.autor == current_user
        )
    )

    if not postagem:
        return abort(404)

    postagem.titulo = data['titulo']
    postagem.gradiente = data['gradiente']
    postagem.visibilidade = data['visibilidade']

    if postagem.corpo != data['corpo']:
        postagem.estado = (
            Estado.APROVADA
                if current_user.role != Role.ALUNO
                else moderar_postagem(data['corpo'])
        )
        postagem.corpo = data['corpo']
    db.session.commit()

    return postagem, 200


@postagens_bp.route('/<int:postagem_id>', methods=['POST'])
@postagens_bp.arguments(schema=PostagemPostSchema)
@postagens_bp.response(201, schema=PostagemSchema)
@jwt_required()
def postar_postagem(data):
    postagem = Postagem(
        titulo=data['titulo'],
        corpo=data['corpo'],
        gradiente=data['gradiente'],
        estado=(
            Estado.APROVADA
                if current_user.role != Role.ALUNO
                else moderar_postagem(data['corpo'])
        ),
        visibilidade=data.get('visibilidade') or Visibilidade.PUBLICADA,
        autor=current_user
    )
    db.session.add(postagem)
    db.session.commit()

    return postagem, 201


@postagens_bp.route('/<int:postagem_id>', methods=['DELETE'])
@postagens_bp.response(204)
@jwt_required()
def delete_postagem(postagem_id):
    postagem = db.session.scalar(
        select(Postagem).where(
            Postagem.autor == current_user,
            Postagem.id == postagem_id
        )
    )

    if not postagem:
        return abort(404)

    db.session.delete(postagem)
    db.session.commit()

    return None
