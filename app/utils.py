import inspect
from functools import wraps
from sanic import response
import string
import random

from .models import Problem, RankedTeam

N = 1.0
n = 1.0

from math import exp, floor, log

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
        SELECT (problem_no, solved, attempts_left) FROM team{team_id}
    """
    problem_records = await db.fetchall(query)
    answers = await db.fetchall(f"SELECT answers FROM team{team_id}")

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

async def fetch_teams(db):
    query = f"""
        SELECT teamname, problems_solved, RANK() OVER ( ORDER BY problems_solved DESC ) rank_number FROM rankings;
    """
    record_rows = await db.fetchall(query)

    teams = []
    for record_row in record_rows:
        teams.append(RankedTeam(
            teamname=record_row[0],
            problems_solved=record_row[1],
            rank=record_row[2]
        ))
    
    print("TEAMNAME: ", teams[0].teamname)
    
    return teams

async def fetch_team_stats(teamname):
    teams = await fetch_teams()
    for team in teams:
        if team.teamname == teamname:
            return team
    return None 

