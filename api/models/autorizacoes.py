from datetime import datetime

from sqlalchemy import DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Autorizacao(Base):
    __tablename__ = "autorizacao_fauna"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    regional: Mapped[str] = mapped_column(Text(), nullable=False)
    municipio: Mapped[str] = mapped_column(Text(), nullable=False)
    tipo: Mapped[str] = mapped_column(Text(), nullable=False)
    protocolo: Mapped[str] = mapped_column(Text(), nullable=False)
    formulario: Mapped[str] = mapped_column(Text(), nullable=False)
    numero_licenca: Mapped[str] = mapped_column(Text(), nullable= False)
    atividade: Mapped[str] = mapped_column(Text(), nullable= False)
    emissao: Mapped[str] = mapped_column(Text(), nullable=False)
    vencimento: Mapped[str] = mapped_column(Text(), nullable=False)
    empreendedor: Mapped[str] = mapped_column(Text(), nullable= False)
    empreendimento: Mapped[str] = mapped_column(Text(), nullable= False)
    bacia_hidrografica: Mapped [str] = mapped_column(Text(), nullable=False)
    capturado_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable= False)
    atualizado_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now(), onupdate= func.now(), nullable= False)

