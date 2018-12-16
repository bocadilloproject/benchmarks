if __name__ == "__main__":
    from os.path import dirname, join
    from frameworks.common import run_gunicorn

    run_gunicorn(
        cwd=join(dirname(__file__), "hello_app"),
        app="hello_app.wsgi:application",
        worker="meinheld",
    )
