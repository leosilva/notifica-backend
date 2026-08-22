from cloudinary import uploader
from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import abort
from sqlalchemy import select

from app import db
from app.auth.models import Role
from app.auth.permissions import roles_required
from app.postagens import postagens_bp
from app.postagens.models import Postagem, Visibilidade
from app.postagens.moderacao import moderar_postagem
from app.postagens.schemas import (
    PostagemImagemSchema,
    PostagemPostSchema,
    PostagemQuerySchema,
    PostagemSchema,
)

# TODOs:
# - implementar views de administração ex:
# (listagem de postagens em revisão,
# update de estado e deleção de conteúdo)
# - condensação de imagens para display no carrossel


@postagens_bp.route('/me')
@postagens_bp.arguments(PostagemQuerySchema, location='query')
@postagens_bp.response(200, PostagemSchema(many=True, exclude=['autor']))
@jwt_required()
@roles_required(Role.ALUNO)
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
@roles_required(Role.ALUNO)
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
@postagens_bp.arguments(schema=PostagemPostSchema, location='form')
@postagens_bp.response(200, PostagemSchema(exclude=['autor']))
@jwt_required()
@roles_required(Role.ALUNO)
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
    postagem.gradiente = data.get('gradiente', None)
    postagem.visibilidade = data['visibilidade']

    if postagem.corpo != data['corpo']:
        postagem.estado = (
            moderar_postagem(data['corpo'])
        )
        postagem.corpo = data['corpo']

    imagem = request.files.get('imagem')
    if imagem and imagem.filename != '':
        res = uploader.upload(imagem)
        postagem.imagem = res.get('secure_url')

    db.session.commit()

    return postagem, 200


@postagens_bp.route('/', methods=['POST'])
@postagens_bp.arguments(
    schema=PostagemPostSchema,
    location='form'
)
@postagens_bp.arguments(
    schema=PostagemImagemSchema,
    location='files'
)
@postagens_bp.response(201, schema=PostagemSchema)
@jwt_required()
@roles_required(Role.ALUNO)
def postar_postagem(data, files):
    imagem = files.get('imagem')
    gradiente = data.get('gradiente')

    if bool(imagem) == bool(gradiente):
        return abort(400)

    postagem = Postagem(
        titulo=data['titulo'],
        corpo=data['corpo'],
        gradiente=gradiente,
        estado=moderar_postagem(data['corpo']),
        visibilidade=data.get('visibilidade') or Visibilidade.PUBLICADA,
        autor=current_user
    )

    if imagem and imagem.filename != '':
        res = uploader.upload(imagem)
        postagem.imagem = res.get('secure_url')
    elif gradiente:
        postagem.gradiente = gradiente

    db.session.add(postagem)
    db.session.commit()

    return postagem, 201


@postagens_bp.route('/<int:postagem_id>', methods=['DELETE'])
@postagens_bp.response(204)
@jwt_required()
@roles_required(Role.ALUNO)
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
