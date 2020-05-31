import inspect
from functools import wraps

from sanic import response
from sanic.response import html

import string
import random

from .models import Problem, RankedTeam, FinalRankedTeam

import sys

N = 1.0
n = 1.0

from math import exp, floor, log
from decimal import Decimal

def get_stack_variable(name):
    stack = inspect.stack()
    try:
        for frames in stack:
            try:
                frame = frames[0]
                current_locals = frame.f_locals
                if name in current_locals:
                    return current_locals[name]
            finally:
                del frame
    finally:
        del stack

async def render_template(env, tpl,*args, **kwargs):
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

def auth_required(admin_required=False):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            logged_in = request['session'].get('logged_in', False)
            if logged_in:
                if admin_required:
                    is_admin = request['session']['user']['admin']
                    if is_admin:
                        resp = await f(request, *args, **kwargs)
                        return resp
                else:
                    resp = await f(request, *args, **kwargs)
                    return resp
            return response.redirect('/login')
        return decorated_function
    return decorator

def string_generator(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

async def fetch_problems(db, team_id):
    query = f"""
        SELECT (problem_no, solved, attempts) FROM team{team_id}
    """
    problem_records = await db.fetchall(query)
    answers = await db.fetchall(f"SELECT answers FROM team{team_id}")

    problems = []
    for problem_rec, answer_rec in zip(problem_records, answers):
        problems.append(Problem(
            number=problem_rec[0][0],
            solved=problem_rec[0][1],
            attempts=problem_rec[0][2],
            answers=answer_rec[0]
        ))

    
    print(problems[0].answers)
    return problems

async def fetch_teams(db):
    query="""select user_details.user_id, user_details.username, final_rankings.score, RANK() OVER ( ORDER BY final_rankings.score DESC ) rank from user_details,final_rankings where final_rankings.team_id = user_details.user_id;"""
    record_rows = await db.fetchall(query)

    teams = []
    for record_row in record_rows:
        teams.append(FinalRankedTeam(
            id=record_row[0],
            teamname=record_row[1],
            score=record_row[2],
            rank=record_row[3]
        ))
    
    return teams

async def fetch_team_stats(db,team_id):
    teams = await fetch_teams(db)
    for team in teams:
        if team.id == team_id:
            return team
    return None 

async def fetchuser(db, username):
    return await db.fetchrow('SELECT * FROM user_details WHERE username = $1', username)

async def login_user(request, user):
    if request['session'].get('logged_in', False):
        return await render_template(request.app.env, 'home.html', user=user)
    request['session']['logged_in'] = True
    request['session']['user'] = user.to_dict()

def float_eq(f1, f2):
    # f1 is real answer
    return abs(f1 - f2) < sys.float_info.epsilon

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) < error * answer