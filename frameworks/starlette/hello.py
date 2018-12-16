from starlette.applications import Starlette
from starlette.responses import PlainTextResponse

app = Starlette()


@app.route("/")
async def index(request):
    return PlainTextResponse("Hello, World!")


if __name__ == "__main__":
    from os.path import dirname, abspath
    from frameworks.common import run_gunicorn

    cwd = dirname(abspath(__file__))

    run_gunicorn(
        cwd=dirname(__file__),
        app="hello:app",
        worker="uvicorn",
    )

