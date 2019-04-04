import sqlite3
import datetime
from flask import Flask, render_template, g, request, redirect, url_for

PATH = 'db/book.sqlite'

app = Flask(__name__)


def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@app.route('/books')
def index():
    return render_template('index.html')

@app.route('/comics')
def comics():
    comics = execute_sql('SELECT * FROM comics')
    return render_template('comics.html', comics=comics)

@app.route('/cookbooks')
def cookbooks():
    cookbooks = execute_sql('SELECT * FROM cookbooks')
    return render_template('cookbooks.html', cookbooks=cookbooks)

@app.route('/classics')
def classics():
    classics = execute_sql('SELECT * FROM classics')
    return render_template('classics.html', classics=classics)


if __name__ == '__main__':
    app.run(debug=True)
