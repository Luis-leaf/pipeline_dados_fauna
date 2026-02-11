from fastapi import APIRouter, Depends, status
from security.api_key import validate_api_key
from sqlalchemy import select
from sqlalchemy.orm import Session

from infra_db.database import get_db
from models.autorizacoes import Autorizacao
from schemas.autorizacao import AutorizacaoRead
from schemas.payload import Query

router = APIRouter(prefix="/autorizacao", tags=["Autorizacao"], dependencies=[Depends(validate_api_key)])


@router.get("", response_model=list[AutorizacaoRead], status_code= status.HTTP_200_OK)
def list_autorizacoes(db: Session = Depends(get_db)):
    aa = db.execute(select(Autorizacao).order_by(Autorizacao.id)).scalars().all()
    return aa


@router.post("/query", response_model=list[AutorizacaoRead], status_code= status.HTTP_200_OK)
def query_autorizacoes(payload: Query, db: Session = Depends(get_db)):
    sql_query = select(Autorizacao)

    for field, value in payload.filters.items():
        column = getattr(Autorizacao, field)
        sql_query = sql_query.where(column == value)

    order_column = getattr(Autorizacao, payload.order_by)

    if payload.order_dir == "asc":
        sql_query= sql_query.order_by(order_column.asc())
    else:
        sql_query = sql_query.order_by(order_column.desc())

    # pagination
    sql_query = sql_query.limit(payload.limit)
    sql_query = sql_query.offset(payload.offset)

    result = db.execute(sql_query).scalars().all()
    return result



