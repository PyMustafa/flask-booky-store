from flask import Flask, render_template, redirect, url_for, flash, request
from forms import AuthorForm, BookForm
from models import db, Author, Book
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_author.html', form=form)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    form.author_id.choices = [(a.id, a.name) for a in Author.query.all()]
    if form.validate_on_submit():
        image_file = form.image.data
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = f'uploads/{filename}'
            print(f"Image uploaded: {image_url}")
        else:
            image_url = 'uploads/default.jpg'
            print("Default image used")

        book = Book(
            name=form.name.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate_age=form.appropriate_age.data,
            author_id=form.author_id.data,
            image_url=image_url
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html', form=form)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    print(f"Image URL: {book.image_url}")
    return render_template('book.html', book=book)

@app.route('/author/<int:author_id>')
def author_details(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('author_details.html', author=author)


@app.route('/authors')
def authors():
    all_authors = Author.query.all()
    return render_template('authors_list.html', authors=all_authors)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")
    app.run(debug=True)
