from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db
from app.auth.models import Usuario


class Postagem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    autor: so.Mapped['Usuario'] = so.relationship(back_populates='postagens')
    autor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('usuario.id'))
    titulo: so.Mapped[str] = so.mapped_column(sa.String(128))
    corpo: so.Mapped[str] = so.mapped_column(sa.String(324))
    imagem: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=True)
    gradiente: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    criado_em: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now)
    atualizado_em: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(),
        default=datetime.now,
        onupdate=datetime.now
    )
