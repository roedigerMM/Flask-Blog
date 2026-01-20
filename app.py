from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json', 'r') as handle:
        blog_posts = json.load(handle)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)