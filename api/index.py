from flask import Flask, request
import json

from OnlySnarf.classes.message import Message, Post

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    args = json.loads(request.data)
    print(args)
    print("Messaging...")
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
    message.send(args["user"])

    return "", 200

@app.route('/post', methods=['POST'])
def post():
    args = json.loads(request.data)
    print(args)
    print("Posting...")
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
    post.send()

    return "", 200

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")