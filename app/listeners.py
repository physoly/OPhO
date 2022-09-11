from app.config import Config
from app.db import AsyncPostgresDB

from sanic import Blueprint, Sanic

from app.db import initialize_team
import aiohttp
from dhooks import Webhook, Embed

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
    #app.ctx.sse_token = await app.ctx.db.fetchval('SELECT token from auth_tokens')
    #webhook_url = await app.ctx.db.fetchval('SELECT url FROM webhook_url')
   # app.ctx.session = aiohttp.ClientSession(loop=loop)
#app.ctx.webhook = Webhook.Async(webhook_url, session=app.ctx.session)


@listeners.listener('after_server_stop')
async def server_end(app, loop):
    await app.ctx.db.close()