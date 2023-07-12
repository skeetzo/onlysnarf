from flask import Flask, request
import json

from OnlySnarf.classes.message import Post

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run():
    args = json.loads(request.data)
    print(args)
    print("Posting...")
    post = Post()
    post.text = args["text"]
    post.files = [args["input"]]
    post.send()

    return "", 200

if __name__ == "__main__":
    app.debug = True
    app.run()