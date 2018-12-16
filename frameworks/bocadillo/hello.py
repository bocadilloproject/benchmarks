import sys
from bocadillo import API

api = API()


@api.route("/")
async def hello(req, res):
    res.text = "Hello, World!"


if __name__ == '__main__':
    host, port = sys.argv[1:3]
    api.run(host=host, port=int(port))
