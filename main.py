from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

# '''
# Make sure the required packages are installed: 
# Open the Terminal in PyCharm (bottom left). 

# On Windows type:
# python -m pip install -r requirements.txt

# On MacOS type:
# pip3 install -r requirements.txt

# This will install the packages from the requirements.txt for this project.
# '''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return self.title

class BlogForm(FlaskForm):
    title = StringField("Blog Post Title")
    subtitle = StringField("Subtitle")
    author = StringField("Your Name")
    img_url = StringField("Blog Image URL")
    body = CKEditorField('Blog content')
    submit = SubmitField('Submit Post')

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = []
    results = db.session.execute(db.Select(BlogPost).order_by(BlogPost.title))
    posts = results.scalars().all()
    # print(posts)
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/<post_id>', methods=["GET","POST"])
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    # print(requested_post)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/new_post", methods=["GET","POST"])
def add_new_post():
    print("its here1")
    form = BlogForm()
    if form.validate_on_submit():
        print("its here2")
        new_blog = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            author = form.author.data,
            img_url = form.img_url.data,
            body = form.body.data,
            date=date.today().strftime("%B %d, %Y")
        )
        print(new_blog.author)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/')
    
    return render_template("make-post.html", form=form)

# TODO: edit_post() to change an existing blog post
@app.route("/edit_post/<post_id>", methods=["GET","POST"])
def edit_post(post_id):
    form = BlogForm()
    post = db.get_or_404(BlogPost, post_id)
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.author.data = post.author
    form.img_url.data = post.img_url
    form.body.data = post.body
    if form.validate_on_submit():
        print("Its here 3")
        item = db.get_or_404(BlogPost, post_id)
        form = BlogForm()
        item.title = form.title.data
        item.subtitle = form.subtitle.data
        item.author = form.author.data
        item.img_url = form.img_url.data
        print(form.body.data)
        item.body = form.body.data
        item.date=date.today().strftime("%B %d, %Y")
        # db.session.add(item)
        db.session.commit()
        # get_item = BlogPost.query.get(post_id)
        # print(get_item.body)
        return redirect('/')    
    return render_template("make-post.html", form=form)

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
