from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def fetch_post_by_id(post_id):
    with open('blog_posts.json', 'r') as handle:
        posts = json.load(handle)

    for post in posts:
        if post['id'] == post_id:
            return post

    return None



@app.route('/')
def index():
    with open('blog_posts.json', 'r') as handle:
        blog_posts = json.load(handle)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        # Load existing posts
        with open('blog_posts.json', 'r') as handle:
            posts = json.load(handle)

        # Generate new ID
        if posts:
            new_id = max(post['id'] for post in posts) + 1
        else:
            new_id = 1

        # Create new post object
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        # Append new post
        posts.append(new_post)

        # Save back to JSON file
        with open('blog_posts.json', 'w') as handle:
            json.dump(posts, handle, indent=4)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):

    # Load existing posts
    with open('blog_posts.json', 'r') as handle:
        posts = json.load(handle)

    # Filter out the post to delete
    updated_posts = [post for post in posts if post['id'] != post_id]

    # Save updated list back to file
    with open('blog_posts.json', 'w') as handle:
        json.dump(updated_posts, handle, indent=4)

    # Redirect back to home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):

    # Load all posts
    with open('blog_posts.json', 'r') as handle:
        posts = json.load(handle)

    # Find requested post
    post = None
    for p in posts:
        if p['id'] == post_id:
            post = p
            break

    if post is None:
        return "Post not found", 404

    # Handle form submit
    if request.method == 'POST':

        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        # Save updated list
        with open('blog_posts.json', 'w') as handle:
            json.dump(posts, handle, indent=4)

        return redirect(url_for('index'))

    # GET request → show update form
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)