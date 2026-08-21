from datetime import datetime
from enum import Enum

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class Role(Enum):
    ADMIN = 'admin'
    SERVIDOR = 'servidor'
    ALUNO = 'aluno'


class Usuario(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(255))
    matricula: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)
    role: so.Mapped[Role] = so.mapped_column(sa.Enum(Role), default=Role.ALUNO)
    criado_em: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now)
    atualizado_em: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(),
        default=datetime.now,
        onupdate=datetime.now
    )
