from app.config import Config
from app.db import AsyncPostgresDB

from sanic import Blueprint, Sanic

from app.db import initialize_team

listeners = Blueprint('listeners')

@listeners.listener('before_server_start')
async def server_begin(app, loop):
    app.ctx.db = AsyncPostgresDB(
        user=Config.DB_USERNAME,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        db_name=Config.DB_NAME,
        loop=loop
    )
    
    await app.ctx.db.init();

@listeners.listener('after_server_stop')
async def server_end(app, loop):
    await app.ctx.db.close()