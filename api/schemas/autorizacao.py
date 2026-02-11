from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AutorizacaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    regional: str
    municipio: str
    tipo: str
    protocolo: str
    formulario: str
    numero_licenca: str
    atividade: str
    emissao: str
    vencimento: str
    empreendedor: str
    empreendimento: str
    bacia_hidrografica: str
    capturado_at: datetime
    atualizado_at: datetime



