import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web


@aiohttp_jinja2.template("auth.html")
async def auth_get(request: web.Request):
    db = request.app['database']
    users = await db.users.get_user('test')
    print(request.get("user", None))
    print(request.get("last_visited", None))
    return {'users': users}


async def auth_post(request: web.Request):
    """ Local user Authentication
       ---
      tags:
      - Authentication
      description: gLocal user Authentication
      parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            username:
               type: string
            password:
                type: string
          required:
            - username
      responses:
        '200':
          description: OK
          schema:
            type: object
            properties:
              authenticated: string
        '400':
          description: Validation error
    """
    authenticated = False
    json_data = await request.json()
    username = json_data.get("username", None)
    password = json_data.get("password", None)
    db = request.app['database']

    user_data = await db.users.get_user(username)
    if user_data:
        # TODO CRYPT PASSWORD
        if user_data["password"] == password:
            authenticated = True

    response_data = {
        "authenticated": authenticated
    }
    if authenticated:
        session = await get_session(request)
        session['user'] = username
        return web.json_response(response_data, status=200)
    else:
        return web.json_response(response_data, status=401)


async def logout(request: web.Request):
    session = await get_session(request)
    if session.get("user", None):
        session.clear()
