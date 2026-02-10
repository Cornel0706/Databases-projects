from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db = SQLAlchemy(app, model_class=Base)

class Book(db.Model):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html', books = db.session.execute(db.select(Book).order_by(Book.title)).scalars())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/modify-rating/<int:id>", methods=["GET", "POST"])
def modify_rating(id):
    book = db.session.get(Book, id)
    if request.method == "POST":
        book.rating = float(request.form["rating"]) 
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('modify_rating.html', book=book)

@app.route("/delete/<int:id>")
def delete_book(id):
    book = db.session.get(Book, id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


