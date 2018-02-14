import asyncpg


class Users:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.__pool = pool

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

    async def get_user(self, user_name: str) -> dict:
        async with self.__pool.acquire() as con:
            row = await con.fetchrow("""
                SELECT 
                    login,
                    password 
                FROM 
                    users
                WHERE
                    login = $1
                """, user_name)
            return {
                    'login': row[0],
                    'password': row[1]
                    }


