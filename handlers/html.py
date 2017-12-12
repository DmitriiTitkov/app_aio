from aiohttp import web
import templates
import aiohttp_jinja2


def template(*args):
    def wrapper():
        return web.web_fileresponse(templates.html)

    return wrapper


@aiohttp_jinja2.template('home.html')
async def home(request: web.Request):
    return {'test': ""}

@aiohttp_jinja2.template('home.html')
async def home_post(request: web.Request):
    print("home_post")
    return {'test': "testVal"}
