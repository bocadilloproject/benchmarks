class App:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        })
        await send({
            "type": "http.response.body",
            "body": b"Hello, World!",
        })


if __name__ == "__main__":
    from os.path import dirname
    from frameworks.common import run_gunicorn

    run_gunicorn(
        cwd=dirname(__file__),
        app="hello:App",
        worker="uvicorn",
    )
