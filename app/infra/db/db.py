# app/infra/db/db.py
from contextlib import asynccontextmanager

from app.infra.db.crud import DB
from app.infra.db.pgsql import async_session_maker


@asynccontextmanager
async def get_db():
    async with async_session_maker() as session:
        yield DB(session)
