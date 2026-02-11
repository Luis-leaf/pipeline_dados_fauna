from typing import Any

from pydantic import BaseModel, field_validator

ALLOWED_FIELDS = {
    "id",
    "regional",
    "municipio",
    "tipo",
    "protocolo",
    "formulario",
    "numero_licenca",
    "atividade",
    "emissao",
    "vencimento",
    "empreendedor",
    "empreendimento",
    "bacia_hidrografica",
    "capturado_at",
    "atualizado_at",
}


class Query(BaseModel):
    fields: list[str]
    filters: dict[str,Any]
    order_by: str = "id"
    order_dir: str = "asc"
    limit: int = 50
    offset: int = 0


    @field_validator("fields")
    @classmethod
    def validate_fields(cls, fields: list[str]) -> list[str]:
        invalid = [field for field in fields if field not in ALLOWED_FIELDS]
        if invalid:
            raise ValueError(f"fields inválidos: {invalid}")
        return fields


    @field_validator("filters")
    @classmethod
    def validate_filters(cls, filters: dict[str,Any]) -> dict[str,Any]:
        invalid = [field for field in filters if field not in ALLOWED_FIELDS]
        if invalid:
            raise ValueError(f"filtros invélidos para os campos: {invalid}")
        return filters


    @field_validator("order_by")
    @classmethod
    def validate_order_by(cls, field: str) -> str:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"order_by inválido: {field}")
        return field


    @field_validator("limit")
    @classmethod
    def validate_limit(cls, limit: int) -> int:
        if limit < 1 or limit > 500:
            raise ValueError("limit deve estar entre 1 e 500")
        return limit


    @field_validator("offset")
    @classmethod
    def validate_offset(cls, offset: int) -> int:
        if offset < 0:
            raise ValueError("offset deve ser >= 0")
        return offset
