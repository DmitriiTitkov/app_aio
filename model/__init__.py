import asyncpg
from .users import Users


class Database:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.pool = pool
        self.users = Users(self.pool)

    async def close(self) -> None:
        await self.pool.close()
