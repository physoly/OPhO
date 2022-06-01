from sanic import Sanic
from sanic_session import Session, InMemorySessionInterface
from jinja2 import Environment, PackageLoader
from sanic_sse import Sse

app = Sanic('OPhO')
Sse(app, url="/events")

from app.listeners import listeners
from app.root import root
from app.opho import opho

from app.config import Config

def create_app(config=Config):
    app.update_config(config)

    app.ctx.env = Environment(loader=PackageLoader('app', 'templates'), enable_async=True)
    Session(app, interface=InMemorySessionInterface())

    app.static('/static', './app/static')
    app.static('/favicon.ico', './app/static/files/favicon.ico?', name='favicon')
    
    app.blueprint(root)
    app.blueprint(opho)
    app.blueprint(listeners)
    
    return app
