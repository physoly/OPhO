from app.utils import render_template, fetch_problems, \
    fetch_team_stats, fetch_teams, fetchuser, login_user, auth_required, float_eq, check_answer, is_advanced, get_all_invi_scores, in_time_open, get_cutoffs, in_time_invi

from app.config import Config
from app.models import RankedTeam, User

from sanic import Blueprint, response, Sanic
import os
from sanic.response import json, HTTPResponse, redirect, json_dumps
from sanic.exceptions import abort

from app.forms import LoginForm

import urllib

import sys

from app.config import Config

import datetime
from http import HTTPStatus

opho = Blueprint('opho', host=f'opho.{Config.DOMAIN}')

from decimal import Decimal
from dhooks import Embed

app = Sanic.get_app()

past_contest_years = [2020, 2021,2022, 2023]

CURRENT_YEAR = 2024

@opho.route('/login', methods=['GET','POST'])
async def _login(request):
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            user_raw = await fetchuser(app.ctx.db, username)
            if user_raw is not None:
                if user_raw['password'] == password:
                    query = "SELECT username FROM admins WHERE username=$1"
                    is_admin = await app.ctx.db.fetchval(query, username)
                    user = User(
                        id=user_raw['user_id'],
                        username=username, 
                        admin=False if is_admin is None else True
                    )
                    res = await login_user(request.ctx.session, user)
                    if not res:
                        return await render_template(app.ctx.env, request, 'home.html', user=user)
                    return response.redirect('/')
            form.username.errors.append('Incorrect username or password')
        return await render_template(app.ctx.env, request, "opho/login.html", form=form)
    return await render_template(app.ctx.env, request, 'opho/login.html', form=LoginForm())

@opho.route('/contest', methods=['GET', 'POST'])
@auth_required()
async def _contest(request):
    admin = request.ctx.session['user']['admin']
    if not admin and not in_time_open():
        return response.redirect('/')

    team_id = request.ctx.session['user']['id']

    if request.method== 'POST':
        return response.redirect('/contest')
    
    not_seen = not await app.ctx.db.fetchval("SELECT seen from seen where team_id=$1", team_id)
    latest_announcement = 0
    if not_seen:
        latest_announcement = await app.ctx.db.fetchval("SELECT msg FROM announcements ORDER BY timestamp DESC LIMIT 1")
    problems = await fetch_problems(db=app.ctx.db, team_id=team_id)
    team_stats = await fetch_team_stats(db=app.ctx.db, team_id=team_id)

    print(problems[0].attempts)

    #TODO upload opho2023_open.pdf to static files and add to gitignore
    return await render_template(
        app.ctx.env,
        request,
        "opho/contest.html", 
        team_stats=team_stats, 
        latest_announcement=json_dumps(latest_announcement),
        problems=sorted(problems, 
        key=lambda x: x.number)
    )

@opho.route('/invitational')
@auth_required()
async def _invi(request):
    user = request.ctx.session['user']
    admin = user['admin']
    team_id = user['id']

    qualified = await is_advanced(app.ctx.db, team_id, 2024)

    if not qualified or not in_time_invi():
        return json({'message': 'Access denied: Your team has not qualified for the invitational.'})
    not_seen = not await app.ctx.db.fetchval("SELECT seen from seen where team_id=$1", team_id)
    latest_announcement = 0
    if not_seen:
        latest_announcement = await app.ctx.db.fetchval("SELECT msg FROM announcements ORDER BY timestamp DESC LIMIT 1")
    return await render_template(app.ctx.env, request, "opho/invi.html", latest_announcement=json_dumps(latest_announcement))
    
@opho.route('/<year>/rankings')
async def _rankings(request, year):
    year = int(year)
    if year == CURRENT_YEAR:
        return await render_template(app.ctx.env, request, "opho/leaderboard.html", ranked_teams=await fetch_teams(app.ctx.db, year))
    if year not in past_contest_years:
        return response.redirect('/archives')
    cutoffs = await get_cutoffs(app.ctx.db, year)
    print(cutoffs)
    return await render_template(app.ctx.env, request, "opho/rankings.html", ranked_teams=await fetch_teams(app.ctx.db, year), cutoffs=await get_cutoffs(app.ctx.db, year))

@opho.route('/<year>/invitational_rankings')
async def _invi_rankings(request,year):
    if int(year) not in past_contest_years:
        return response.redirect('/archives')
    if int(year) == 2021 or int(year) == 2022 or int(year) == 2023:
        return await render_template(app.ctx.env, request, f"opho/invi_rankings_{year}.html", invi_records=await app.ctx.db.fetchall(f'SELECT * FROM invi_scores_{year}'))
    return await render_template(app.ctx.env, request, f"opho/invi_rankings_{year}.html", invi_records=await get_all_invi_scores(app.ctx.db, year))

@opho.post('/api/answer_submit')
@auth_required()
async def _answer_submit(request):
    auth_token = request.headers.get('Authorization', None)

    admin = request.ctx.session['user']['admin']
    if not admin and not in_time_open():
        return response.json({'error' : 'unauthorized'}, status=401)

    payload = dict(urllib.parse.parse_qs(str(request.body, 'utf8')))

    problem_no = int(payload['problem_no'][0])

    team_answer = Decimal(payload['answer'][0])
    team_id = request.ctx.session['user']['id']
    current = await app.ctx.db.fetchrow(f"SELECT * from team{team_id} WHERE problem_no = $1", problem_no)

    if current['solved'] or current['attempts'] >= 3:
        return response.json({'error': 'forbidden'}, status=403)
    print("REQUEST IP", request.remote_addr)
    await app.ctx.db.execute_job("INSERT INTO log(team_id, problem_no, ip, answer, attempt_no, timestamp) VALUES ($1,$2,$3, $4,$5, current_timestamp)", team_id, problem_no, request.remote_addr, team_answer, current['attempts']+1)

    real_answer = await app.ctx.db.fetchval(f"SELECT (answer) FROM problems WHERE problem_no=$1", problem_no)
    error_bound = await app.ctx.db.fetchval("SELECT (error_bound) FROM problems where problem_no=$1", problem_no)
    is_correct = check_answer(attempt=team_answer, answer=real_answer, error=error_bound)

    solve_data = await app.ctx.db.fetchrow(
            f"UPDATE team{team_id} SET solved=$1, attempts = attempts + 1, answers=array_append(answers, $2), timestamp = current_timestamp WHERE problem_no = $3 and attempts < 3 RETURNING *;",
            is_correct, team_answer, problem_no
    )
    
    if is_correct:
        await app.ctx.db.execute_job(f"""
            UPDATE rankings_2024 SET score = score + 1 WHERE team_id=$1
        """, team_id
        )

    stats = await fetch_team_stats(app.ctx.db, team_id)   

    return response.json({
        'correct' : is_correct, 
        'attempts_left' : 3 - solve_data['attempts'], 
        'answers' : solve_data['answers'], 
        'rank' : stats.rank, 
        'problems_solved' : stats.score
    })

@opho.post('/api/seen')
async def _seen(request):
    data = request.json
    team_id = request.ctx.session['user']['id']
    if data['seen']:
        await app.ctx.db.execute_job("UPDATE seen SET seen='t' WHERE team_id=$1", team_id)
    return json({"status": "ok"})

@opho.post('/api/announcements')
async def _announcements(request):
    auth_token = request.headers.get('Authorization', None)
    channel_id = request.json.get("channel_id")
    msg = request.json['msg']
    webhook = request.json.get('webhook',False)
    await app.ctx.db.execute_job(f"INSERT INTO announcements(msg) VALUES ('{msg}')")
    if auth_token == app.ctx.sse_token:
        try:
            await request.app.sse_send(msg, channel_id=channel_id)
        except KeyError:
            abort(HTTPStatus.NOT_FOUND, "channel not found")
        
        await app.ctx.db.execute_job("UPDATE seen SET seen='f'")
        if webhook:
            em = Embed(color=0x2ecc71, timestamp='now')
            em.set_author('Announcement', icon_url='https://cdn.discordapp.com/attachments/782105673928146984/984431266516598844/unknown.png')
            em.description = msg
            em.set_footer(text='https://opho.physoly.tech/announcements', icon_url='https://cdn.discordapp.com/attachments/782105673928146984/984431266516598844/unknown.png')
            await app.ctx.webhook.send(embed=em)
        return json({"status":"ok"})
    return response.json({'error' : 'unauthorized'}, status=401)

"""
@app.route('/admin/createcontest', methods=['GET', 'POST'])
#@auth_required(admin_required=True)
async def _create_contest(request):
    request = app

    query_string = "INSERT INTO problems(problem_no, answer) VALUES "
    value_strings = []

    if request.method == 'POST':
        contest_name = request.form.pop('contestname')[0]
        values = request.form.values()

        for i, field in enumerate(values):
            value_strings.append(f"({i+1}, {field[0]})")
        query = query_string + ', '.join(value_strings) + ';'
        await create_problem_table(db=app.ctx.db, contest_name=contest_name)
        #await app.ctx.db.execute_job(query)
    return await template('opho/create_contest.html')
"""

@opho.route('/')
async def _contest_home(request):
    return await render_template(app.ctx.env, request, 'opho/contest_home.html', in_time_open=in_time_open(),in_time_invi=in_time_invi())

@opho.get('/logout')
async def _logout(request):
    request.ctx.session.clear()
    return response.redirect('/')

@opho.get('/announcements')
async def _announcements(request):
    announcements = await app.ctx.db.fetchall('SELECT * FROM announcements ORDER BY timestamp DESC')
    fmt_timestamps = []
    for an in announcements:
        fmt_timestamps.append(an['timestamp'].strftime("%m/%d/%Y, %H:%M:%S"))
    announcements = zip(fmt_timestamps, announcements)
    return await render_template(app.ctx.env, request, 'opho/announcements.html', announcements=announcements)

@opho.get('/team')
async def _team(request):
    return await render_template(app.ctx.env, request, 'opho/team.html')

@opho.get('/winners')
async def _winners(request):
    return await render_template(app.ctx.env, request, 'opho/winners.html')

@opho.get('/info', name='opho_info')
async def _opho_info(request):
    return await render_template(app.ctx.env, request, 'opho.html')

@opho.get('/archives')
async def _archives(request):
    return await render_template(app.ctx.env, request, 'opho/archives.html')