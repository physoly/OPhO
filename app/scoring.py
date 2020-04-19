from .utils import fetch_problems, fetch_teams

from collections import namedtuple
from .models import ScoredUser

from math import exp, log, floor

UserProblem = namedtuple('UserProblem', ['team_id', 'problem'])

problem_data = {}
user_scores = {}

num_problems = 30

def get_problem_score(num_attempts, solve_pos, num_solved, num_attempted):
    c1 = pow(0.9, num_attempts)
    c2 = exp(num_solved / 30) + max(8 - floor(log(num_attempted), 2))
    c3 = 0.3 * solve_pos

    return c1 * c2 * c3

async def fill_problem_data(db):
    teams = await fetch_teams()
    for team in teams:
        problems = await fetch_problems(id=team.id)
        for problem in problems:
            problem_data[problem.number].append(UserProblem(team_id=team.id, problem=problem))

def sort_problems():
    for i in range(1, num_problems + 1):
        problem_data[i] = sorted(problem_data[i], key=lambda x: x.problem.timestamp)

def get_scores():
    for problem_number, user_problems in problem_data:
        num_solved, num_attempted = get_solved_and_attempted(user_problems)

        for idx, user_problem in enumerate(user_problems):
            prev = user_scores.get(user_problem.team_id, 0)
            
            score = get_problem_score(
                num_attempts=user_problem.problem.attempts,
                solve_pos=idx + 1,
                num_solved=num_solved,
                num_attempted=num_attempted
            )

            user_scores[user_problem.team_id] = prev + score


def get_solved_and_attempted(user_problems):
    num_solved = 0
    num_attempted = 0

    for user_problem in user_problems:
        problem = user_problem.problem
        if problem.solved:
            num_solved += 1
        if problem.attempted > 0: 
            num_attempted += 1
    
    return (num_solved, num_attempted)