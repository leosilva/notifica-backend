import enum
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db
from app.auth.models import Usuario
from app.postagens.models import Visibilidade


class Fonte(enum.Enum):
    G1 = 'g1'
    METROPOLES = 'metropoles'
    UOL = 'uol'
    CNN = 'cnn'


class Noticia(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    titulo: so.Mapped[str] = so.mapped_column(sa.String(255))
    corpo: so.Mapped[str] = so.mapped_column(sa.Text())
    url: so.Mapped[str | None] = so.mapped_column(sa.String(512), nullable=True, unique=True)
    imagem: so.Mapped[str | None] = so.mapped_column(sa.String(512), nullable=True)
    fonte: so.Mapped[Fonte | None] = so.mapped_column(sa.Enum(Fonte), nullable=True)
    autor: so.Mapped[Usuario | None] = so.relationship(back_populates='noticias')
    autor_id: so.Mapped[int | None] = so.mapped_column(sa.ForeignKey('usuario.id'), nullable=True)
    visibilidade: so.Mapped[Visibilidade] = so.mapped_column(
        sa.Enum(Visibilidade),
        default=Visibilidade.PUBLICADA
    )
    publicado_em: so.Mapped[datetime | None] = so.mapped_column(sa.DateTime(), nullable=True)
    criado_em: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now)
    atualizado_em: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(),
        default=datetime.now,
        onupdate=datetime.now
    )
