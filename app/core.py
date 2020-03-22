from sanic import Sanic, response
from sanic.response import html, text, json, HTTPResponse, redirect

from sanic_session import Session, InMemorySessionInterface

from app import app

import ujson

import aiohttp

session_interface = Session(app, interface=InMemorySessionInterface())

app.config.AUTH_LOGIN_ENDPOINT = 'login'

with open("./config/config.json") as f:
    global_config = ujson.loads(f.read())

app.config.SECRET_KEY = global_config['SECRET_KEY']

@app.listener('before_server_start')
async def server_begin(app, loop):
    app.session = aiohttp.ClientSession(loop=loop)
    # initialize database here

@app.listener('after_server_stop')
async def server_end(app, loop):
    # close database pool here
    await app.session.close()

