from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os
'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

ckeditor = CKEditor()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)
ckeditor.init_app(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

class PostForm(FlaskForm):
    title = StringField()
    subtitle = StringField()
    author = StringField()
    img_url = StringField()
    body = CKEditorField()
    submit = SubmitField()


with app.app_context():
    db.create_all()

# edit flag
is_edit = 0

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = db.session.execute(db.Select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/<post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/create', methods=["POST", "GET"])
def create():
    form = PostForm()
    new_post = BlogPost()
    today = date.today()
    if request.method == "POST":
        new_post.title = form.title.data
        new_post.author = form.author.data
        new_post.body = form.body.data
        new_post.img_url = form.img_url.data
        new_post.subtitle = form.subtitle.data
        new_post.date = today.strftime("%B %d, %Y")
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form, is_edit=is_edit)
# TODO: edit_post() to change an existing blog post
@app.route('/edit_post/<id>', methods=["GET", "POST"])
def edit_post(id):
    is_edit = 1
    post = db.get_or_404(BlogPost, id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if request.method == "POST":
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.author = form.author.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form, is_edit=is_edit)
# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<id>')
def delete(id):
    post = db.get_or_404(BlogPost, id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
