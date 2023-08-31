import os
import json
import logging
from flask import Flask, request

from ..util import CONFIG

def create_app():
    app = Flask(__name__)

    @app.route('/message', methods=['POST'])
    def message():
        try:
            args = json.loads(request.data)
            logging.debug(args)
            CONFIG["text"] = args["text"]
            CONFIG["user"] = args["user"]
            try: CONFIG["input"] = args["input"].split(",")
            except Exception as e: pass
            try: CONFIG["price"] = args["price"] or 0
            except Exception as e: pass
            try: CONFIG["schedule"] = args["schedule"]
            except Exception as e: pass
            try: CONFIG["performers"] = args["performers"]
            except Exception as e: pass
            from ..snarf import Snarf
            Snarf.message()
            Snarf.close()
        except Exception as e:
            logging.debug(e)
        finally:
            return "", 200

    @app.route('/post', methods=['POST'])
    def post():
        try:
            args = json.loads(request.data)
            logging.debug(args)
            CONFIG["text"] = args["text"]
            try: CONFIG["input"] = args["input"].split(",")
            except Exception as e: pass
            try: CONFIG["performers"] = args["performers"]
            except Exception as e: pass
            try: CONFIG["schedule"] = args["schedule"]
            except Exception as e: pass
            try: CONFIG["questions"] = args["questions"]
            except Exception as e: pass
            try: CONFIG["duration"] = args["duration"]
            except Exception as e: pass
            try: CONFIG["expires"] = args["expires"]
            except Exception as e: pass
            from ..snarf import Snarf
            Snarf.post()
            Snarf.close()
        except Exception as e:
            logging.debug(e)
        finally:
            return "", 200

    return app

def main():
    app = create_app()
    if str(CONFIG["debug"]) == "True":
        app.debug = True
        app.testing = True
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()