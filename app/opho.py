from app.utils import render_template, fetch_problems, \
    fetch_team_stats, fetch_teams, fetchuser, login_user, auth_required, float_eq

from app.config import Config
from app.models import RankedTeam, User

from sanic import Blueprint, response
from sanic.response import json, HTTPResponse, redirect

from app.forms import LoginForm

import urllib

import sys

from app.config import Config

opho = Blueprint('opho', host=f'opho.{Config.DOMAIN}:{Config.PORT}')

from decimal import Decimal

@opho.route('/login', methods=['GET','POST'])
async def _login(request):
    app = request.app
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            user_raw = await fetchuser(app.db, username)
            if user_raw is not None:
                if user_raw['password'] == password:
                    query = "SELECT username FROM admins WHERE username=$1"
                    is_admin = await app.db.fetchval(query, username)
                    await login_user(request, User(
                        id=user_raw['user_id'],
                        username=username, 
                        admin=False if is_admin is None else True
                    ))
                    return response.redirect('/')
            form.username.errors.append('Incorrect username or password')
        return await render_template(app.env, "opho/login.html", form=form)
    return await render_template(app.env, 'opho/login.html', form=LoginForm())

@opho.route('/contest', methods=['GET', 'POST'])
@auth_required()
async def _contest_home(request):
    app = request.app

    team_id = request['session']['user']['id']

    if request.method== 'POST':
        return response.redirect('/contest')

    problems = await fetch_problems(db=app.db, team_id=team_id)
    team_stats = await fetch_team_stats(db=app.db, team_id=team_id)

    print(problems[0].attempts)

    return await render_template(
        app.env,
        "opho/contest.html", 
        team_stats=team_stats, 
        problems=sorted(problems, 
        key=lambda x: x.number)
    )


@opho.route('/rankings')
async def _rankings(request):
    app = request.app
    return await render_template(app.env, "opho/rankings.html", ranked_teams=await fetch_teams(app.db))

@opho.post('/api/answer_submit')
@auth_required()
async def _answer_submit(request):
    app = request.app

    auth_token = request.headers.get('Authorization', None)

    if auth_token is None or auth_token != Config.API_AUTH_TOKEN:
        return response.json({'error' : 'unauthorized'}, status=401)

    payload = dict(urllib.parse.parse_qs(str(request.body, 'utf8')))

    problem_no = int(payload['problem_no'][0])

    team_answer = Decimal(payload['answer'][0])
    team_id = request['session']['user']['id']

    real_answer = await app.db.fetchval(f"SELECT (answer) FROM problems WHERE problem_no=$1", problem_no)

    is_correct = float_eq(real_answer, team_answer)

    solved_str = 't' if is_correct else 'f'
    
    solve_data = await app.db.fetchrow(
            f"UPDATE team{team_id} SET solved=$1, attempts = attempts + 1, answers=array_append(answers, $2), timestamp = current_timestamp WHERE problem_no = $3 and attempts < 3 RETURNING *;",
            is_correct, team_answer, problem_no
    )

    duplicate = solve_data['answers'].count(team_answer)

    if is_correct:
        await app.db.execute_job(f"""
            UPDATE rankings SET problems_solved = problems_solved + 1 WHERE team_id=$1
        """, team_id
        )

    stats = await fetch_team_stats(app.db, team_id)   

    return response.json({
        'correct' : is_correct, 
        'attempts_left' : 3 - solve_data['attempts'], 
        'answers' : solve_data['answers'], 
        'rank' : stats.rank, 
        'problems_solved' : stats.problems_solved 
    })

"""
@app.route('/admin/createcontest', methods=['GET', 'POST'])
#@auth_required(admin_required=True)
async def _create_contest(request):
    request = request.app

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
"""

@opho.route('/')
async def _contest_home(request):
    app = request.app
    return await render_template(app.env, 'opho/contest_home.html')

@opho.get('/logout')
async def _logout(request):
    request['session'].clear()
    return response.redirect('/')

@opho.get('/team')
async def _team(request):
    app = request.app
    return await render_template(app.env, 'opho/team.html')