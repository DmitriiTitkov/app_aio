import asyncpg
import json
from .users import Users


class Database:
    def __init__(self):
        self.config = {}

    @classmethod
    async def create(cls, config_path: str):
        self = Database()
        self.config = json.load(open('config/database.json'))
        pool = await self.__create_pool()
        self.users = Users(pool)
        return self

    async def __create_pool(self) -> asyncpg.pool.Pool:
        return await asyncpg.create_pool(self.config["databaseconfig"]["dsn"],
                                         min_size=self.config["databaseconfig"]["minsize"],
                                         timeout=self.config["databaseconfig"]["timeout"])


