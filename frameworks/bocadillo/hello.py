from bocadillo import API

api = API()


@api.route("/")
async def hello(req, res):
    res.text = "Hello, World!"


if __name__ == "__main__":
    from os.path import dirname
    from frameworks.common import run_gunicorn

    run_gunicorn(
        cwd=dirname(__file__),
        app="hello:api",
        worker="uvicorn",
    )
