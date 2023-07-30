import json
from flask import Flask, request

from .util.config import config
from .util.settings import Settings
from .snarf import Snarf

def create_app():
    app = Flask(__name__)

    @app.route('/message', methods=['POST'])
    def message():
        try:
            return "", 200
        finally:
            args = json.loads(request.data)
            Settings.dev_print(args)
            config["text"] = args["text"]
            config["user"] = args["user"]
            try: config["files"] = args["input"].split(",")
            except Exception as e: pass
            try: config["price"] = args["price"] or 0
            except Exception as e: pass
            try: config["schedule"] = args["schedule"]
            except Exception as e: pass
            try: config["performers"] = args["performers"]
            except Exception as e: pass
            if app.testing:
                config["debug"] = True
                config["verbose"] = 3
            print("messaging")
            Snarf.message()
            Snarf.close()

    @app.route('/post', methods=['POST'])
    def post():
        try:
            return "", 200
        finally:
            args = json.loads(request.data)
            Settings.dev_print(args)
            config["text"] = args["text"]
            try: config["files"] = args["input"].split(",")
            except Exception as e: pass
            try: config["performers"] = args["performers"]
            except Exception as e: pass
            try: config["schedule"] = args["schedule"]
            except Exception as e: pass
            try: config["questions"] = args["questions"]
            except Exception as e: pass
            try: config["duration"] = args["duration"]
            except Exception as e: pass
            try: config["expires"] = args["expires"]
            except Exception as e: pass
            if app.testing:
                config["debug"] = True
                config["verbose"] = 3
            print("posting")
            Snarf.post()
            Snarf.close()

    return app

def main():
    app = create_app()
    app.debug = True
    app.testing = True
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()