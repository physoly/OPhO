from .db import db_execute_job

class User():
    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    @classmethod
    async def new_user(cls, username, password):
        # TODO: maybe encrypt credentials
        await db_execute_job('INSERT INTO user_credentials (username,password) VALUES (1,2)', username, password)
        return cls(id=1, username=username)