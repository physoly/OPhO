import inspect
from functools import wraps

from sanic import response
from sanic.response import html

import string
import random

from .models import Problem, RankedTeam

import sys

N = 1.0
n = 1.0

from math import exp, floor, log
from decimal import Decimal

import datetime

OPEN_START_DAY = 12
OPEN_END_DAY = 15
OPEN_START_MONTH = 8
OPEN_END_MONTH = 8

INVI_START_DAY = 29
INVI_END_DAY = 2
INVI_START_MONTH = 8
INVI_END_MONTH = 9

INVI_START = datetime.datetime(2024, 8, 26)
INVI_END = datetime.datetime(2024, 8, 27)

# Adjust the logic for end time
def in_time_open():
    utc_now = datetime.datetime.utcnow()

    # Check if today is the last day and time is within the 4-hour extended period
    if utc_now.month == OPEN_END_MONTH and utc_now.day == OPEN_END_DAY:
        end_time = datetime.datetime(utc_now.year, OPEN_END_MONTH, OPEN_END_DAY, 4)  # 4 AM UTC of the last day
        in_extended_time = utc_now < end_time
    else:
        in_extended_time = False

    # Check if the current date is within the open period or within the extended 4 hours on the last day
    right_month = utc_now.month >= OPEN_START_MONTH and utc_now.month <= OPEN_END_MONTH
    right_day = (utc_now.day >= OPEN_START_DAY and utc_now.day < OPEN_END_DAY) or (utc_now.day == OPEN_END_DAY and in_extended_time)
    
    print("IN TIME", right_month and right_day)
    return right_month and right_day

def in_time_invi():
    utc_now = datetime.datetime.utcnow()
    return utc_now >= INVI_START and utc_now < INVI_END

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

async def render_template(env, request, tpl,*args, **kwargs):
    template = env.get_template(tpl)
    # request = get_stack_variable('request')
    user = None
    if request.ctx.session.get('logged_in'):
        user = request.ctx.session['user']
    kwargs['request'] = request
    kwargs['session'] = request.ctx.session
    kwargs['user'] = user
    # kwargs.update(globals())
    return html(await template.render_async(*args,**kwargs))

async def is_advanced(db, team_id, year):
    return await db.fetchval(f'SELECT score FROM rankings_{year} WHERE team_id = $1', team_id) > 0

def auth_required(admin_required=False):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            logged_in = request.ctx.session.get('logged_in', False)
            if logged_in:
                if admin_required:
                    is_admin = request.ctx.session['user']['admin']
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

async def fetch_teams(db, year):
    final_rankings_table = f"rankings_{year}"
    query=f"""select user_details_{year}.user_id, user_details_{year}.username, {final_rankings_table}.score, RANK() OVER ( ORDER BY {final_rankings_table}.score DESC ) rank from user_details_{year},{final_rankings_table} where {final_rankings_table}.team_id = user_details_{year}.user_id;"""
    record_rows = await db.fetchall(query)

    teams = []
    for record_row in record_rows:
        teams.append(RankedTeam(
            id=record_row[0],
            teamname=record_row[1],
            score=record_row[2],
            rank=record_row[3]
        ))
    
    return teams

async def fetch_team_stats(db,team_id):
    teams = await fetch_teams(db, 2024)
    for team in teams:
        if team.id == team_id:
            return team
    return None 

async def fetchuser(db, username):
    return await db.fetchrow('SELECT * FROM user_details_2024 WHERE username = $1', username)

async def login_user(session, user):
    if session.get('logged_in', False):
        return False
    session['logged_in'] = True
    session['user'] = user.to_dict()
    return True

async def get_all_invi_scores(db, year):
    scores = await db.fetchall(f'SELECT * FROM invi_scores_{year}')
    return sorted(scores, key=lambda x: x['rank'])

def float_eq(f1, f2):
    # f1 is real answer
    return abs(f1 - f2) < sys.float_info.epsilon

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) <= abs(error * answer)

async def get_cutoffs(db, year):
    vals = await db.fetchall(f'SELECT * from cutoffs_{year}')
    print(vals)
    return await db.fetchall(f'SELECT * from cutoffs_{year}')
