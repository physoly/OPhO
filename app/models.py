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
    def __init__(self, number, solved, attempts_remaining, answers):
        self.number = number
        self.solved = solved
        self.id = "Problem " + str(self.number)
        self.attempts_remaining = attempts_remaining
        self.answers = answers

class RankedTeam():
    def __init__(self, teamname, problems_solved):
        self.teamname = teamname
        self.problems_solved = problems_solved
    