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
    def __init__(self, number):
        self.number = number
        self.solved = False
        self.id = "Problem " + self.number
        self.attempts_remaining = 0
    