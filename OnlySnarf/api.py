import json
from flask import Flask, request

from .classes.message import Message, Post
from .util.settings import Settings

def create_app():
    app = Flask(__name__)

    @app.route('/message', methods=['POST'])
    def message():
        Settings.dev_print(request.data)
        args = json.loads(request.data)
        Settings.dev_print(args)
        Settings.print("Messaging...")
        message = Message()
        message.text = args["text"]
        try: message.files = args["input"].split(",")
        except Exception as e: pass
        try: message.price = args["price"] or 0
        except Exception as e: pass
        try: message.schedule = args["schedule"]
        except Exception as e: pass
        try: message.performers = args["performers"]
        except Exception as e: pass
        if not app.testing:
            message.send(args["user"])

        return "", 200

    @app.route('/post', methods=['POST'])
    def post():
        Settings.dev_print(request.data)
        args = json.loads(request.data)
        Settings.dev_print(args)
        Settings.print("Posting...")
        post = Post()
        post.text = args["text"]
        try: post.files = args["input"].split(",")
        except Exception as e: pass
        try: post.performers = args["performers"]
        except Exception as e: pass
        try: post.schedule = args["schedule"]
        except Exception as e: pass
        try: post.questions = args["questions"]
        except Exception as e: pass
        try: post.duration = args["duration"]
        except Exception as e: pass
        try: post.expires = args["expires"]
        except Exception as e: pass
        if not app.testing:
            post.send()

        return "", 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")