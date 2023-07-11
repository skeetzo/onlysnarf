from flask import Flask, request, jsonify
import json

from OnlySnarf.classes.message import Post

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run():
    args = json.loads(request.data)
    print(args)
    print("Running - {}".format(args["action"]))
    post = Post()
    post.text = args["text"]
    post.tags = []
    post.files = [args["input"]]
    post.send()

    return "", 200



if __name__ == "__main__":
    app.run()