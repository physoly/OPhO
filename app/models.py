class User():
    def __init__(self, id, username, admin=False):
        self.id = id
        self.username = username
        self.admin = admin
    """
    @classmethod
    async def new_user(cls, username, password):
        # TODO: maybe encrypt credentials
        await db_execute_job('INSERT INTO user_credentials (username,password) VALUES (1,2)', username, password)
        return cls(id=1, username=username)
        """
    
    def to_dict(self):
        return {'id': self.id, 'username' : self.username, 'admin' : self.admin}

class Problem():
    def __init__(self, number, solved, attempts, answers, timestamp=None):
        self.number = number
        self.solved = solved
        self.id = "Problem " + str(self.number)
        self.attempts = attempts
        self.answers = answers
        self.timestamp = timestamp

class RankedTeam():
    def __init__(self, id, teamname, score, rank):
        self.id = id
        self.teamname = teamname
        self.score = score
        self.rank = rank
    
"""
class FinalRankedTeam():
    def __init__(self, id, teamname, score, rank):
        self.id = id
        self.teamname = teamname
        self.score = score
        self.rank = rank
"""
    
class ScoredUser():
    def __init__(self, team_id, score):
        self.team_id = team_id
        self.score = score

class InviRankedTeam():
    def __init__(self, teamname, problem_scores, rank):
        self.teamname = teamname
        self.problem_scores = problem_scores
        self.rank = rank