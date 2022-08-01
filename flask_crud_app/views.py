import random

from flask import render_template, request, redirect
from sqlalchemy import MetaData, create_engine

from flask_crud_app import app
from flask_crud_app.config import DB_CONNECT
from flask_crud_app.db import Database

db = create_engine(DB_CONNECT)
books_table = Database().get_db_structure(table_name='books', meta=MetaData(db))


# allow us to select all books from db and display on web UI
@app.route("/", methods=["GET"])
def get():
    with db.connect() as conn:
        # Create table if it does not exist
        if not books_table.exists(db):
            books_table.create()

        # select all books
        select = conn.execute(books_table.select())

        # code below needed to select exact [1] element from select query, which is 'title'
        titles = []
        [titles.append(item._row[1]) for item in select]

    return render_template('home.html', book_output=titles)


# allow us to add book to db and redirect back to /
@app.route("/", methods=["POST"])
def post():
    book_input = request.form.get('book_input')

    with db.connect() as conn:
        if book_input:
            # Insert book info to db
            insert_query = books_table \
                .insert() \
                .values(book_id=random.randint(1000000, 9999999), title=book_input)
            conn.execute(insert_query)

    render_template('home.html', book=[book_input])
    return redirect("/")


# allow us to update exact book by title and redirect back to /
@app.route("/update", methods=["POST"])
def update():
    with db.connect() as conn:
        new_title = request.form.get("new_title")
        old_title = request.form.get("old_title")

        # select here exact row which matches with the old_title and retrieve book_id from select
        select_old_title = conn.execute(books_table.select().where(books_table.c.title == old_title))
        book_id_old_title = [item._row[0] for item in select_old_title]

        # update exact book with old_title book_id and change it to new_title value
        update_query = books_table \
            .update() \
            .where(books_table.c.book_id == book_id_old_title[0]) \
            .values(title=new_title)
        conn.execute(update_query)

    render_template('home.html', book=[new_title])
    return redirect("/")


# allow us to delete exact book by title and redirect back to /
@app.route("/delete", methods=["POST"])
def delete():
    with db.connect() as conn:
        book_title = request.form.get("title")

        # select here exact row which matches with the title and retrieve book_id_title from select
        select = conn.execute(books_table.select().where(books_table.c.title == book_title))
        book_id_title = [item._row[0] for item in select]

        # delete row filtered by book_id
        delete_query = books_table \
            .delete() \
            .where(books_table.c.book_id == book_id_title[0])
        conn.execute(delete_query)

    render_template('home.html', book=[book_title])
    return redirect("/")
