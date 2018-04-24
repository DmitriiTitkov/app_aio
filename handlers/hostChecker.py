from aiohttp import web
from model import Database
import aiohttp_jinja2


async def host_checker(request: web.Request):
    return aiohttp_jinja2.render_template('hostChecker.html', request, {}, app_key=aiohttp_jinja2.APP_KEY,
                                          encoding='utf-8'
                                          )


async def get_host(request: web.Request, host, port, status):
    """ Returns all hosts defined by user
       ---
      tags:
      - HostChecker
      description: Returns all hosts defined by user
      parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            login:
               type: string
          required:
            - login
      responses:
        '200':
          description: OK
          schema:
            type: object
            properties:
              host: string
              port: string
              status: string
        '400':
          description: Validation error
    """
    print(host, port, status)
    return{}


async def add_host(request: web.Request, host, port, body):
    """ Add host for user
       ---
      tags:
      - HostChecker
      description: Adds host
      parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            host:
               type: string
               minLength: 1
            port:
               type: integer
               minimum: 0
               maximum: 65535
          required:
            - host
            - port
      responses:
        '200':
          description: OK
          schema:
            type: object
            properties:
              message: success
        '400':
          description: Validation error
    """
    db = request.app['database']  # type:Database
    await db.hosts.add_host("test", body["host"], body["port"])
    print(body["host"], body["port"])
    return{}
