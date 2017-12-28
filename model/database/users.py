import asyncpg


class Users:
    def __init__(self, pool):
        self.__pool: asyncpg.pool.Pool = pool

    async def get_all_users(self)-> list:
        async with self.__pool.acquire() as con:
            rows = await con.fetch("""
                SELECT 
                    login,
                    password 
                FROM 
                    users
                """)
            data = []
            for row in rows:
                data.append({
                    'login': row[0],
                    'password': row[1]
                    })
        return data
