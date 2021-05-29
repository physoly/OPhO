from app.utils import render_template
from app.config import Config

from sanic import Blueprint, response, Sanic
from sanic.response import json, HTTPResponse, redirect

root = Blueprint('root', host=Config.DOMAIN)

app = Sanic.get_app()

@root.get('/')
async def _home(request):
    return await render_template(app.ctx.env, "home.html")

@root.get('/opho')
async def _opho_info(request):
    url = app.url_for('opho.opho_info')
    return response.redirect(url)

@root.get('/kalda')
async def _kalda(request):
    return await render_template(app.ctx.env, request, "kalda.html")

@root.get('/resources')
async def _resources(request):
    return await render_template(app.ctx.env, request, "resources.html")

@root.get('/team')
async def _physoly_team(request):
    return await render_template(app.ctx.env,request, "team.html")

@root.get('/problems')
async def _problems(request):
    return await render_template(app.ctx.env, request, "problems.html")

@root.get('/potd')
async def _problems(request):
    return await render_template(app.ctx.env,request, "potd.html")

