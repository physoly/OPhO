from app.utils import render_template
from app.config import Config

from sanic import Blueprint, response
from sanic.response import json, HTTPResponse, redirect

root = Blueprint('root')

@root.get('/')
async def _home(request):
    return await render_template(request.app.env, "home.html")

@root.get('/opho')
async def _opho_info(request):
    url = request.app.url_for('opho.opho_info')
    return response.redirect(url)

@root.get('/kalda')
async def _kalda(request):
    return await render_template(request.app.env, "kalda.html")

@root.get('/resources')
async def _resources(request):
    return await render_template(request.app.env, "resources.html")

@root.get('/problems')
async def _problems(request):
    return await render_template(request.app.env, "problems.html")

@root.get('/resources')
async def _resources(request):
    return await render_template(request.app.env, "resources.html")
