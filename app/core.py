from app import app

from sanic import Sanic, response
from sanic.response import html, text, json, HTTPResponse, redirect
from sanic_session import Session, InMemorySessionInterface

import ujson
import aiohttp
from jinja2 import Environment, PackageLoader

from .utils import get_stack_variable, auth_required
from .db import AsyncPostgresDB, create_team_table
from .forms import LoginForm, CreateContestForm
from .models import User, Problem

import urllib
import sys
from decimal import Decimal

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
    #await create_team_table(app.db, "tigers", 30)
    #print(await app.db.fetchall("SELECT answers FROM johnny"))

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
                    await login_user(request, User(id=user_raw['user_id'], username=username))
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
    teamname = request['session']['user']['username']
    if request.method== 'POST':
        print("FORM POST: ",request.form)
        return response.redirect('/contest')

    problems = await fetch_problems(teamname=teamname)
    return await template("contest.html", problems=sorted(problems, key=lambda x: x.number))

@app.post('/api/answer_submit')
async def _answer_submit(request):
    auth_token = request.headers['Authorization']

    if auth_token not in global_config['auth_tokens']:
        return response.json({'error' : 'unauthorized'}, status=401)

    payload = dict(urllib.parse.parse_qs(str(request.body, 'utf8')))

    problem_no = payload['problem_no'][0]
    team_answer = float(payload['answer'][0])
    teamname = payload['teamname'][0]

    real_answer = await app.db.fetchval(f"SELECT (answer) FROM problems WHERE problem_no={problem_no}")

    is_correct = abs(float(real_answer) - team_answer) < sys.float_info.epsilon

    solved_str = 't' if is_correct else 'f'
    
    attempts_left = await app.db.fetchval(
            f"UPDATE {teamname} SET solved='{solved_str}', attempts_left = attempts_left - 1, answers=array_append(answers, {team_answer}) WHERE problem_no = {problem_no} and attempts_left > 0 RETURNING attempts_left;"
        )

    if attempts_left is None:
        return response.json({'correct': False, 'attempts_left': 0})        

    return response.json({'correct' : is_correct, 'attempts_left' : attempts_left})

@app.route('/admin/createcontest', methods=['GET', 'POST'])
async def _create_contest(request):
    if request.method == 'POST':
        form = request.form
        for field in request.form.values():
            val = field[0]
            print(val)
    return await template('create_contest.html')

async def fetchuser(username):
    return await app.db.fetchrow('SELECT * FROM user_details WHERE username = $1', username)

async def login_user(request, user):
    if request['session'].get('logged_in', False):
        return await template('home.html', user=user)
    request['session']['logged_in'] = True
    request['session']['user'] = user.to_dict()

async def fetch_problems(teamname):
    query = f"""
        SELECT (problem_no, solved, attempts_left) FROM {teamname}
    """
    problem_records = await app.db.fetchall(query)
    answers = await app.db.fetchall(f"SELECT answers FROM {teamname}")

    problems = []
    for problem_rec, answer_rec in zip(problem_records, answers):
        problems.append(Problem(
            number=problem_rec[0][0],
            solved=problem_rec[0][1],
            attempts_remaining=problem_rec[0][2],
            answers=answer_rec[0]
        ))

    
    print(problems[0].answers)
    return problems

async def add_answer(teamname, answer, problem_number):
    query = f"""
        UPDATE {teamname} SET answers = array_append(answers, {answer}) WHERE 
    """
    await app.db.execute_job(query)

@app.get('/logout')
async def _logout(request):
    request['session'].clear()
    return text('logged out')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False