from app import app

from sanic import Sanic, response
from sanic.response import html, text, json, HTTPResponse, redirect
from sanic_session import Session, InMemorySessionInterface
from sanic.blueprints import Blueprint


import ujson
import aiohttp
from jinja2 import Environment, PackageLoader

from .utils import get_stack_variable, auth_required, string_generator, fetch_problems, fetch_team_stats, fetch_teams
from .db import AsyncPostgresDB, initialize_team, create_problem_table
from .forms import LoginForm, CreateContestForm
from .models import User, Problem, RankedTeam

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

bp = Blueprint("")

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
    app.db = AsyncPostgresDB(dsn=global_config['remote_psql_dsn'], user=global_config['psql_username'], loop=app.loop)
    await app.db.init();
    #await initialize_team(app.db, "testuser", "pass", 6)
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
                    query = f"SELECT username FROM admins WHERE username='{username}'"
                    is_admin = await app.db.fetchval(query)
                    await login_user(request, User(
                        id=user_raw['user_id'],
                        username=username, 
                        admin=False if is_admin is None else True
                    ))
                    return response.redirect('/contesthome')
            form.username.errors.append('Incorrect username or password')
        return await template("opho/login.html", form=form)
    return await template('opho/login.html', form=LoginForm())

@app.get('/')
async def _home(request):
    return await template("home.html")

@app.route('/contest', methods=['GET', 'POST'])
@auth_required()
async def _contest_home(request):
    team_id = request['session']['user']['id']

    if request.method== 'POST':
        return response.redirect('/contest')

    problems = await fetch_problems(db=app.db, team_id=team_id)
    team_stats = await fetch_team_stats(db=app.db, team_id=team_id)

    print(problems[0].attempts)

    return await template("opho/contest.html", team_stats=team_stats, problems=sorted(problems, key=lambda x: x.number))


@app.route('/rankings')
async def _rankings(request):
    return await template("opho/rankings.html", ranked_teams=await fetch_teams(app.db))

@app.post('/api/answer_submit')
@auth_required()
async def _answer_submit(request):
    auth_token = request.headers.get('Authorization', None)

    if auth_token is None or auth_token not in global_config['auth_tokens']:
        return response.json({'error' : 'unauthorized'}, status=401)

    payload = dict(urllib.parse.parse_qs(str(request.body, 'utf8')))

    problem_no = payload['problem_no'][0]

    team_answer = float(payload['answer'][0])
    team_id = request['session']['user']['id']

    real_answer = await app.db.fetchval(f"SELECT (answer) FROM problems WHERE problem_no={problem_no}")

    is_correct = abs(float(real_answer) - team_answer) < sys.float_info.epsilon

    solved_str = 't' if is_correct else 'f'
    
    solve_data = await app.db.fetchrow(
            f"UPDATE team{team_id} SET solved='{solved_str}', attempts = attempts + 1, answers=array_append(answers, {team_answer}), timestamp = current_timestamp WHERE problem_no = {problem_no} and attempts < 3 RETURNING *;"
    )

    if is_correct:
        await app.db.execute_job(f"""
            UPDATE rankings SET problems_solved = problems_solved + 1 WHERE team_id={team_id}
        """
        )

    stats = await fetch_team_stats(app.db, team_id)   

    return response.json({
        'correct' : is_correct, 
        'attempts_left' : 3 - solve_data['attempts'], 
        'answers' : solve_data['answers'], 
        'rank' : stats.rank, 
        'problems_solved' : stats.problems_solved 
    })

@app.route('/admin/createcontest', methods=['GET', 'POST'])
#@auth_required(admin_required=True)
async def _create_contest(request):
    query_string = "INSERT INTO problems(problem_no, answer) VALUES "
    value_strings = []

    if request.method == 'POST':
        contest_name = request.form.pop('contestname')[0]
        values = request.form.values()

        for i, field in enumerate(values):
            value_strings.append(f"({i+1}, {field[0]})")
        query = query_string + ', '.join(value_strings) + ';'
        await create_problem_table(db=app.db, contest_name=contest_name)
        #await app.db.execute_job(query)
    return await template('opho/create_contest.html')

@app.route('/contesthome')
async def _contest_home(request):
    return await template('opho/contest_home.html')

@app.get('/opho')
async def _opho_promo(request):
    return await template('rob.html')

async def fetchuser(username):
    return await app.db.fetchrow('SELECT * FROM user_details WHERE username = $1', username)

async def login_user(request, user):
    if request['session'].get('logged_in', False):
        return await template('home.html', user=user)
    request['session']['logged_in'] = True
    request['session']['user'] = user.to_dict()

@app.get('/logout')
async def _logout(request):
    request['session'].clear()
    return response.redirect('/')

