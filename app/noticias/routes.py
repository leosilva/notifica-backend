from cloudinary import uploader
from flask_jwt_extended import current_user, jwt_required
from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import db
from app.auth.models import Role
from app.auth.permissions import roles_required
from app.noticias import noticias_bp
from app.noticias.models import Noticia, Visibilidade
from app.noticias.schemas import (
    NoticiaImagemSchema,
    NoticiaPostSchema,
    NoticiaQuerySchema,
    NoticiaSchema,
)


@noticias_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required(Role.ADMIN, Role.SERVIDOR)
@noticias_bp.arguments(schema=NoticiaPostSchema, location='form')
@noticias_bp.arguments(schema=NoticiaImagemSchema, location='files')
@noticias_bp.response(201, schema=NoticiaSchema(exclude=['autor']))
def postar_noticia(data, files):
    noticia = Noticia(
        titulo=data['titulo'],
        corpo=data['corpo'],
        url=data.get('url'),
        autor=current_user,
        visibilidade=data.get('visibilidade') or Visibilidade.PUBLICADA,
    )

    imagem = files.get('imagem')
    pub_id = None

    try:
        if imagem and imagem.filename != '':
            res = uploader.upload(imagem)
            noticia.imagem = res.get('secure_url')

            pub_id = res['public_id']

        db.session.add(noticia)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        if pub_id:
            uploader.destroy(pub_id)

        abort(409, message='URL já existente.')

    return noticia


@noticias_bp.route('/')
@jwt_required()
@roles_required(Role.ADMIN, Role.SERVIDOR)
@noticias_bp.arguments(NoticiaQuerySchema, location='query')
@noticias_bp.response(200, schema=NoticiaSchema(many=True, exclude=['autor']))
def minhas_noticias(query):
    stmt = select(Noticia).where(Noticia.autor == current_user)

    visibilidade = query.get('visibilidade')
    if visibilidade:
        stmt = stmt.where(Noticia.visibilidade == visibilidade)

    return db.session.scalars(
        stmt
    ).all()


@noticias_bp.route('/<int:noticia_id>')
@jwt_required()
@roles_required(Role.ADMIN, Role.SERVIDOR)
@noticias_bp.response(200, schema=NoticiaSchema(exclude=['autor']))
def detail_noticia(noticia_id):
    noticia = db.session.scalar(
        select(Noticia).where(
            Noticia.autor == current_user, Noticia.id == noticia_id
        )
    )

    if not noticia:
        return abort(404, message='Nenhuma notícia encontrada.')

    return noticia


@noticias_bp.route('/<int:noticia_id>', methods=['PUT'])
@jwt_required()
@roles_required(Role.ADMIN, Role.SERVIDOR)
@noticias_bp.arguments(schema=NoticiaPostSchema, location='form')
@noticias_bp.arguments(schema=NoticiaImagemSchema, location='files')
@noticias_bp.response(200, schema=NoticiaSchema(exclude=['autor']))
def atualizar_noticia(data, files, noticia_id):
    noticia = db.session.scalar(
        select(Noticia).where(
            Noticia.id == noticia_id,
            Noticia.autor == current_user
        )
    )

    if not noticia:
        return abort(404, message='Nenhuma notícia encontrada.')

    noticia.titulo = data['titulo']
    noticia.corpo = data['corpo']
    noticia.url = data.get('url')

    if data.get('visibilidade'):
        noticia.visibilidade = data.get('visibilidade')

    imagem = files.get('imagem')

    if bool(imagem) and imagem.filename != '':
        res = uploader.upload(imagem)
        noticia.imagem = res.get('secure_url')

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return abort(409, message='URL já existente.')

    return noticia, 200


@noticias_bp.route('/<int:noticia_id>', methods=['DELETE'])
@jwt_required()
@roles_required(Role.ADMIN, Role.SERVIDOR)
@noticias_bp.response(204)
def delete_noticia(noticia_id):
    noticia = db.session.scalar(
        select(Noticia).where(
            Noticia.id == noticia_id, Noticia.autor == current_user
        )
    )

    if not noticia:
        return abort(404)

    db.session.delete(noticia)
    db.session.commit()

    return
