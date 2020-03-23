from app import app

from sanic import Sanic, response
from sanic.response import html, text, json, HTTPResponse, redirect
from sanic_session import Session, InMemorySessionInterface

import ujson
import aiohttp
from jinja2 import Environment, PackageLoader

from .utils import get_stack_variable
from .db import AsyncPostgresDB
from .forms import LoginForm
from .models import User

env = Environment(loader=PackageLoader('app', 'templates'))
session_interface = Session(app, interface=InMemorySessionInterface())

app.config.AUTH_LOGIN_ENDPOINT = 'login'

app.static('/static', './app/static')

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
    app.db = AsyncPostgresDB(dsn=global_config['psql_dsn'], user=global_config['psql_username'], loop=app.loop)
    await app.db.init();
    # initialize database here

@app.listener('after_server_stop')
async def server_end(app, loop):
    # close database pool here
    await app.db.close()

@app.route('/login', methods=['GET','POST'])
async def _login(request):
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            user_raw = await fetchuser(username)
            if user_raw is not None:
                if user_raw['password'] == password:
                    login_user(request, User(id=user_raw['user_id'], username=username))
                    return response.text("sucess!")
            form.username.errors.append('Incorrect username or password')
        return template("login.html", form=form)
    return template('login.html', form=LoginForm())

async def fetchuser(username):
    return await app.db.fetchrow('SELECT * FROM user_details WHERE username = $1', username)

def login_user(request, user):
    if request['session'].get('logged_in', False):
        return template('home.html', user=user)
    request['session']['logged_in'] = True
    request['session']['user'] = user.to_dict()