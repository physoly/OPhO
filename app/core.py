from app import app

from sanic import Sanic, response
from sanic.response import html, text, json, HTTPResponse, redirect
from sanic_session import Session, InMemorySessionInterface

import ujson
import aiohttp
from jinja2 import Environment, PackageLoader

from .utils import get_stack_variable, auth_required
from .db import AsyncPostgresDB, create_team_table
from .forms import LoginForm, ContestForm
from .models import User, Problem


env = Environment(loader=PackageLoader('app', 'templates'), enable_async=True)
session_interface = Session(app, interface=InMemorySessionInterface())

app.config.AUTH_LOGIN_ENDPOINT = 'login'

app.static('/static', './app/static')

with open("./config/config.json") as f:
    global_config = ujson.loads(f.read())

app.config.SECRET_KEY = global_config['SECRET_KEY']

async def template(tpl, *args, **kwargs):
    template = env.get_template(tpl)
    request = get_stack_variable('request')
    user = None
    if request['session'].get('logged_in'):
        user = request['session']['user']
    kwargs['request'] = request
    kwargs['session'] = request['session']
    kwargs['user'] = user
    kwargs.update(globals())
    return html(await template.render_async(*args,**kwargs))

@app.listener('before_server_start')
async def server_begin(app, loop):
    app.db = AsyncPostgresDB(dsn=global_config['local_psql_dsn'], user=global_config['local_psql_username'], loop=app.loop)
    await app.db.init();
    #await create_team_table(app.db, "johnny", 30)

@app.listener('after_server_stop')
async def server_end(app, loop):
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
                    return response.redirect('/contest')
            form.username.errors.append('Incorrect username or password')
        return await template("login.html", form=form)
    return await template('login.html', form=LoginForm())

@app.get('/')
async def _home(request):
    return await template("home.html")

@app.route('/contest', methods=['GET', 'POST'])
@auth_required()
async def _contest_home(request):
    if request.method== 'POST':
        answer = list(request.form.values())[0][0]
        # query problem answer database and verify it
        # if correct, add a point, update question in team database
        # if incorrect, remove an attempt
        return response.redirect('/contest')
    problems = await fetch_problems(teamname=request['session']['user']['username'])
    form = ContestForm()
    print(len(form.problems))
    return await template("contest.html", form=form, problems_and_input=sorted(list(zip(problems,form.problems)), key=lambda x: x[0].number))

async def fetchuser(username):
    return await app.db.fetchrow('SELECT * FROM user_details WHERE username = $1', username)

def login_user(request, user):
    if request['session'].get('logged_in', False):
        return template('home.html', user=user)
    request['session']['logged_in'] = True
    request['session']['user'] = user.to_dict()

async def fetch_problems(teamname):
    query = f"""
        SELECT (problem_no, solved, attempts_left) FROM {teamname} 
    """
    problem_records = await app.db.fetchall(query)
    return [Problem.record_to_problem(record[0]) for record in problem_records]