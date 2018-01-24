import asyncpg
from aiohttp import web
from .users import Users


class Database:
    def __init__(self):
        self.config = {}
        self.pool: asyncpg.pool.Pool = None

    @classmethod
    async def create(cls, app: web.Application):
        self = Database()
        self.config = app['database_config']
        self.pool = await self.__create_pool()
        self.users = Users(self.pool)

        app['database'] = self

    async def close(self):
        await self.pool.close()

    async def __create_pool(self) -> asyncpg.pool.Pool:
        return await asyncpg.create_pool(self.config["databaseconfig"]["dsn"],
                                         min_size=self.config["databaseconfig"]["minsize"],
                                         timeout=self.config["databaseconfig"]["timeout"])



