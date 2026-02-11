from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import Any


class FaunaDb:
    TABLE_NAME = "autorizacao_fauna"
    COLUMNS = (
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
    )

    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            db_path = Path(__file__).resolve().parent / "db.sqlite"
        self.db_path = Path(db_path)

    def insert_dict_fauna(self, dict_fauna: Mapping[str, Any]) -> int:
        data = self._filter_data(dict_fauna)
        if not data:
            raise ValueError("dict_fauna has no valid columns to insert")

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({placeholders})"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(sql, tuple(data.values()))
            return int(cursor.lastrowid)

    def update_dict_fauna(self, row_id: int, dict_fauna: Mapping[str, Any]) -> None:
        data = self._filter_data(dict_fauna)
        if not data:
            return

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE id = ?"

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql, (*data.values(), row_id))

    def exists_by_protocolo(self, protocolo: str) -> bool:
        sql = f"SELECT 1 FROM {self.TABLE_NAME} WHERE protocolo = ? LIMIT 1"
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(sql, (protocolo,)).fetchone()
            return row is not None

    def _filter_data(self, dict_fauna: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: dict_fauna[key]
            for key in self.COLUMNS
            if key in dict_fauna and dict_fauna[key] is not None
        }
