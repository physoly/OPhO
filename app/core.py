from app import app

from sanic import Sanic, response
from sanic.response import html, text, json, HTTPResponse, redirect
from sanic_session import Session, InMemorySessionInterface

import ujson
import aiohttp
from jinja2 import Environment, PackageLoader

from .utils import get_stack_variable
from .db import AsyncPostgresDB

env = Environment(loader=PackageLoader('app', 'templates'))
session_interface = Session(app, interface=InMemorySessionInterface())

app.config.AUTH_LOGIN_ENDPOINT = 'login'

with open("./config/config.json") as f:
    global_config = ujson.loads(f.read())

app.config.SECRET_KEY = global_config['SECRET_KEY']

def template(tpl, *args, **kwargs):
    template = env.get_template(tpl)
    request = get_stack_variable('request')
    user = None
    if request['session'].get('logged_in'):
        user = request['session']['user']
    kwargs['request'] = request
    kwargs['session'] = request['session']
    kwargs['user'] = user
    kwargs.update(globals())
    return html(template.render(*args,**kwargs))

@app.listener('before_server_start')
async def server_begin(app, loop):
    app.session = aiohttp.ClientSession(loop=loop)
    app.db = AsyncPostgresDB(dsn="0.0.0.0", user="ben", loop=app.loop)
    await app.db.init();
    # initialize database here

@app.listener('after_server_stop')
async def server_end(app, loop):
    # close database pool here
    await app.session.close()
    await app.db.close()

