from flask import Flask, render_template, redirect, url_for, flash, request, session, g, jsonify
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import AuthorForm, BookForm, RegistrationForm, LoginForm
from models import db, Author, Book, User, bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.context_processor
def inject_user():
    return dict(user=g.user)


@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_author.html', form=form, title="Add Author")


@app.route('/edit_author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if form.validate_on_submit():
        author.name = form.name.data
        db.session.commit()
        flash('Author updated successfully!', 'success')
        return redirect(url_for('author_details', author_id=author.id))

    return render_template('add_author.html', form=form, title="Edit Author")


@app.route('/delete_author/<int:author_id>', methods=['POST'])
@login_required
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)

    if author.books:
        flash("Cannot delete author with associated books. Delete the books first.", "danger")
        return redirect(url_for('author_details', author_id=author_id))

    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully!', 'success')
    return redirect(url_for('authors'))


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
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
    return render_template('add_book.html', form=form, title="Add Book")


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm()
    form.author_id.choices = [(a.id, a.name) for a in Author.query.all()]

    if request.method == 'GET':
        form.name.data = book.name
        if isinstance(book.publish_date, str):
            from datetime import datetime
            try:
                form.publish_date.data = datetime.strptime(book.publish_date, '%Y-%m-%d').date()
            except ValueError:
                form.publish_date.data = None
        else:
            form.publish_date.data = book.publish_date
        form.price.data = book.price
        form.appropriate_age.data = book.appropriate_age
        form.author_id.data = book.author_id

    if form.validate_on_submit():
        book.name = form.name.data
        book.publish_date = form.publish_date.data
        book.price = form.price.data
        book.appropriate_age = form.appropriate_age.data
        book.author_id = form.author_id.data

        # Handle image update
        if form.image.data:
            image_file = form.image.data
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                book.image_url = f'uploads/{filename}'

        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book_details', book_id=book.id))

    return render_template('add_book.html', form=form, title="Edit Book", book=book)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('index'))


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['user_id'] = user.id
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")
    app.run(debug=True)