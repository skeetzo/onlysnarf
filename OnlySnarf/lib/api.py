import os
import json
import logging
logger = logging.getLogger(__name__)
from flask import Flask, request

from .driver import close_browser
from ..classes.discount import Discount
from ..classes.message import Message, Post

def create_app():
    app = Flask(__name__)

    @app.route('/discount', methods=['POST'])
    def discount():
        try:
            logger.debug("received discount request:")
            args = json.loads(request.data)
            logger.debug(args)
            discount_object = {
                "amount" : args.get("amount", 0),
                "months" : args.get("months", 0),
                "username" : args.get("username", "")
            }
            if not app.debug:
                Discount.create_discount(discount_object).apply()
                # keep open when done: default false
                if not args.get("keep", False):
                    close_browser()
        except Exception as e:
            logger.debug(e)
        finally:
            return "", 200

    @app.route('/message', methods=['POST'])
    def message():
        try:
            logger.debug("received message request:")
            args = json.loads(request.data)
            logger.debug(args)
            message_object = {
                "text" : args.get("text", ""),
                "recipients" : args.get("recipients", []),
                "files" : args.get("files", []),
                "price" : args.get("price", 0),
                "schedule" : args.get("schedule", {}),
                "performers" : args.get("performers", []),
                "keywords" : args.get("keywords", []),
                "includes" : args.get("includes", []),
                "excludes" : args.get("excludes", [])
            }
            if not app.debug:
                Message.create_message(message_object).send()
                # keep open when done: default false
                if not args.get("keep", False):
                    close_browser()
        except Exception as e:
            logger.debug(e)
        finally:
            return "", 200

    @app.route('/post', methods=['POST'])
    def post():
        try:
            logger.debug("received post request:")
            args = json.loads(request.data)
            logger.debug(args)
            post_object = {
                "text" : args.get("text", ""),
                "recipients" : args.get("recipients", []),
                "files" : args.get("files", []),
                "price" : args.get("price", 0),
                "schedule" : args.get("schedule", {}),
                "performers" : args.get("performers", []),
                "keywords" : args.get("keywords", []),
                "questions" : args.get("questions", []),
                "duration" : args.get("duration", []),
                "expires" : args.get("expires", 0)
            }
            if not app.debug:
                Post.create_post(post_object).send()
                # keep open when done: default false
                if not args.get("keep", False):
                    close_browser()
        except Exception as e:
            logger.debug(e)
        finally:
            return "", 200

    return app

def main(debug=False):
    app = create_app()
    if debug:
        app.debug = True
        app.testing = True
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()