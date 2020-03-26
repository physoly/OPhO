class User():
    def __init__(self, id, username):
        self.id = id
        self.username = username
    """
    @classmethod
    async def new_user(cls, username, password):
        # TODO: maybe encrypt credentials
        await db_execute_job('INSERT INTO user_credentials (username,password) VALUES (1,2)', username, password)
        return cls(id=1, username=username)
        """
    
    def to_dict(self):
        return {'id': self.id, 'username' : self.username}

class Problem():
    def __init__(self, number, solved, attempts_remaining):
        self.number = number
        self.solved = solved
        self.id = "Problem " + str(self.number)
        self.attempts_remaining = attempts_remaining
    
    @classmethod
    def record_to_problem(cls, record):
        return cls(
            number=record[0], 
            solved=record[1],
            attempts_remaining=record[2]
        )