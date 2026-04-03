from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

users = []
posts = []

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Post:
    def __init__(self, id, caption, image, user):
        self.id = id
        self.caption = caption
        self.image = image
        self.user = user
        self.likes = 0

# Home
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', posts=posts, user=session['user'])

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users.append(User(username, password))
        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user.username == username and user.password == password:
                session['user'] = username
                return redirect('/')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# Upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')

    caption = request.form['caption']
    file = request.files['image']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        posts.insert(0, Post(len(posts), caption, filename, session['user']))

    return redirect('/')

# Like
@app.route('/like/<int:id>')
def like(id):
    for post in posts:
        if post.id == id:
            post.likes += 1
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)