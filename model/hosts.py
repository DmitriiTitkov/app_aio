import asyncpg


class Hosts:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.__pool = pool

    async def get_hosts(self, user):
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

    async def add_host(self, login, host, port):
        async with self.__pool.acquire() as con:  # type: asyncpg.Connection
            # await con.execute("""insert into hosts ( host, port) values ( $1, $2)""", host, port)

            await con.execute("""with new_host as (
                    insert into hosts (host, port) values ($1, $2)
                    returning host_id)
            insert into user_host (login, host_id)
            values( $3,  (select host_id from new_host));""", host, port, login)

    async def remove_host(self, login, host, port):
        async with self.__pool.acquire() as con:
            con.exequte()