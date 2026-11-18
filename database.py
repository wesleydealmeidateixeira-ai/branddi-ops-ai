
import sqlite3
from datetime import datetime
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "branddi_ops.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def inicializar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS decisoes_gerenciais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                decisao TEXT NOT NULL,
                justificativa TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                capacidade_semanal REAL NOT NULL,
                demanda_semanal REAL NOT NULL,
                fila_inicial INTEGER NOT NULL,
                prazo_semanas INTEGER NOT NULL
            )
        """)


def registrar_decisao(
    decisao,
    justificativa,
    responsavel,
    capacidade_semanal,
    demanda_semanal,
    fila_inicial,
    prazo_semanas
):
    if not all([
        str(decisao).strip(),
        str(justificativa).strip(),
        str(responsavel).strip()
    ]):
        raise ValueError("Decisão, justificativa e responsável são obrigatórios.")

    inicializar_banco()

    with conectar() as conexao:
        cursor = conexao.execute("""
            INSERT INTO decisoes_gerenciais (
                data_hora,
                decisao,
                justificativa,
                responsavel,
                capacidade_semanal,
                demanda_semanal,
                fila_inicial,
                prazo_semanas
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().astimezone().isoformat(timespec="seconds"),
            decisao,
            justificativa,
            responsavel,
            capacidade_semanal,
            demanda_semanal,
            fila_inicial,
            prazo_semanas
        ))

        return cursor.lastrowid


def consultar_decisoes():
    inicializar_banco()

    with conectar() as conexao:
        conexao.row_factory = sqlite3.Row

        registros = conexao.execute("""
            SELECT *
            FROM decisoes_gerenciais
            ORDER BY id DESC
        """).fetchall()

        return [dict(registro) for registro in registros]
