from collections import deque
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import joinedload

from app import db
from app.carrossel.schemas import Tipo
from app.noticias.models import Noticia
from app.postagens.models import Estado, Postagem, Visibilidade


def get_conteudo() -> list[dict[str, Any]]:
    agora = datetime.now()
    limite = agora - timedelta(hours=24)

    postagens = deque(
        db.session.scalars(
            select(Postagem)
            .options(joinedload(Postagem.autor))
            .where(
                Postagem.criado_em >= limite,
                Postagem.estado == Estado.APROVADA,
                Postagem.visibilidade == Visibilidade.PUBLICADA,
            )
            .order_by(Postagem.criado_em.desc())
        ).all()
    )

    noticias = deque(
        db.session.scalars(
            select(Noticia)
            .options(joinedload(Noticia.autor))
            .where(
                Noticia.visibilidade == Visibilidade.PUBLICADA,
                or_(
                    and_(
                        Noticia.vencimento.is_not(None),
                        Noticia.vencimento >= agora,
                    ),
                    and_(
                        Noticia.vencimento.is_(None),
                        Noticia.criado_em >= limite,
                    ),
                ),
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
                'gradiente': noticia.gradiente,
                'vencimento': noticia.vencimento,
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
                'gradiente': postagem.gradiente,
                'visibilidade': postagem.visibilidade,
                'autor': postagem.autor,
                'tipo': Tipo.POSTAGEM,
            })

    return conteudo
