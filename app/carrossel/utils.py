from collections import deque
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app import db
from app.carrossel.schemas import Tipo
from app.noticias.models import Noticia
from app.postagens.models import Estado, Postagem, Visibilidade


def get_conteudo() -> list[dict[str, str | int]]:
    limite = datetime.now() - timedelta(hours=24)

    postagens = deque(
        db.session.scalars(
            select(Postagem)
            .options(joinedload(Postagem.autor))
            .where(
                Postagem.criado_em >= limite,
                Postagem.estado == Estado.APROVADA,
                Postagem.visibilidade == Visibilidade.PUBLICADA
            )
            .order_by(Postagem.criado_em.desc())
        ).all()
    )

    noticias = deque(
        db.session.scalars(
            select(Noticia)
            .options(joinedload(Noticia.autor))
            .where(
                Noticia.criado_em >= limite,
                Noticia.visibilidade == Visibilidade.PUBLICADA,
            )
            .order_by(Noticia.criado_em.desc())
        ).all()
    )

    conteudo: list[dict[str, Any]] = []
    while postagens or noticias:
        for _ in range(5):
            if not noticias:
                break

            noticia = noticias.popleft()
            conteudo.append({
                'id': noticia.id,
                'titulo': noticia.titulo,
                'corpo': noticia.corpo,
                'url': noticia.url,
                'imagem': noticia.imagem,
                'gradiente': None,
                'visibilidade': noticia.visibilidade,
                'autor': noticia.autor,
                'tipo': Tipo.NOTICIA,
            })

        if postagens:
            postagem = postagens.popleft()
            conteudo.append({
                'id': postagem.id,
                'titulo': postagem.titulo,
                'corpo': postagem.corpo,
                'url': None,
                'imagem': postagem.imagem,
                'gradiente': postagem.gradiente,
                'visibilidade': postagem.visibilidade,
                'autor': postagem.autor,
                'tipo': Tipo.POSTAGEM,
            })

    return conteudo
