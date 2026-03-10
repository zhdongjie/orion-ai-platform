# app/infra/db/curd.py
from typing import TypeVar, Type, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class DB:
    """数据库操作封装"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, obj: ModelType, refresh: bool = True) -> ModelType:
        """新增记录"""
        self.session.add(obj)
        await self.session.commit()

        if refresh:
            await self.session.refresh(obj)

        return obj

    async def delete(self, obj: ModelType):
        """删除"""
        await self.session.delete(obj)
        await self.session.commit()

    async def update(self):
        """提交更新"""
        await self.session.commit()

    async def get(self, model: Type[ModelType], obj_id) -> Optional[ModelType]:
        """根据主键获取"""
        return await self.session.get(model, obj_id)

    async def list(
            self,
            model: Type[ModelType],
            limit: int = 100
    ) -> Sequence[ModelType]:
        stmt = select(model).limit(limit)

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def execute(self, stmt):
        """执行自定义 SQL"""
        return await self.session.execute(stmt)

    async def flush(self, obj: Optional[ModelType] = None):
        """将新增对象 flush 到数据库，不 commit"""
        if obj:
            self.session.add(obj)
        await self.session.flush()
