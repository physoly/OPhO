from app import create_app
import sanic.exceptions

app = create_app()

async def handle_not_found(request, exception):
    return sanic.response.empty(status=404)

if __name__ == "__main__":  
    app.run(host="physolydev.tech", port=app.config.PORT)