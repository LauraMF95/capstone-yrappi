from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)
CORS(app)

# Rutas de la aplicación para usar:
## Ruta para obtener todos los libros en React
@app.route('/books', methods=['GET'])
def get_books():
    try:
        cursor = db.database.cursor()
        sql = "SELECT * FROM books"
        cursor.execute(sql)
        datos = cursor.fetchall()
        books = []
        for fila in datos:
            book = {'books_id': fila[0], 'books_name': fila[1], 'books_author': fila[2], 'books_category': fila[3], 'books_position': fila[4], 'books_review': fila[5], 'books_image': fila[6], 'books_date': fila[7], 'books_status': fila[8]}
            books.append(book)
        return jsonify({'books': books, 'mensaje': "Get books"})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})

## Ruta para obtener un libro en React
@app.route('/books/<books_id>', methods=['GET'])
def get_boook(books_id):
    try:
        cursor = db.database.cursor()
        sql = "SELECT * FROM books WHERE books_id = '{0}'".format(books_id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            book = {'books_id': datos[0], 'books_name': datos[1], 'books_author': datos[2], 'books_category': datos[3], 'books_position': datos[4], 'books_review': datos[5], 'books_image': datos[6], 'books_date': datos[7], 'books_status': datos[8]}
            return jsonify({'book': book, 'mensaje': "Get one book" })
        else:
            return jsonify({'mensaje': "Book not found"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

## Ruta para crear un libro en React
@app.route('/submit', methods=['POST'])
def post_book():
    try:
        cursor = db.database.cursor()
        sql = "INSERT INTO books (books_name, books_author, books_category, books_position, books_review, books_image, books_date, books_status) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(request.json['books_name'], request.json['books_author'], request.json['books_category'], request.json['books_position'], request.json['books_review'], request.json['books_image'], request.json['books_date'], request.json['books_status'])
        cursor.execute(sql)
        db.database.commit()
        return jsonify({'mensaje': "Book posted"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
## Ruta para eliminar un libro en React
@app.route('/eliminar/<books_id>', methods=['DELETE'])
def delete_book(books_id):
    try:
        cursor = db.database.cursor()
        sql = "DELETE FROM books WHERE books_id = '{0}'".format(books_id)
        cursor.execute(sql)
        db.database.commit()
        return jsonify({'mensaje': "Book deleted"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
## Ruta para editar un libro en React
@app.route('/update/<books_id>', methods=['PUT'])
def update_book(books_id):
    try:
        cursor = db.database.cursor()
        sql = "UPDATE books SET books_name = '{0}', books_author = '{1}', books_category = '{2}', books_position = '{3}', books_review = '{4}', books_image = '{5}', books_date = '{6}', books_status = '{7}'  WHERE books_id = '{8}'".format(request.json['books_name'], request.json['books_author'], request.json['books_category'], request.json['books_position'], request.json['books_review'], request.json['books_image'], request.json['books_date'], request.json['books_status'], books_id)
        cursor.execute(sql)
        db.database.commit()
        return jsonify({'mensaje': "Book updated"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    

#Rutas de la aplicación para mostrar:
##Ruta para mostrar los libros en la tabla
@app.route('/', methods=['GET'])
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM books")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    return render_template('index.html', data = insertObject)

##Ruta para guardar libros en la base de datos a través de la tabla
@app.route('/book', methods=['POST'])
def addBook():
    books_name = request.form['books_name']
    books_author = request.form['books_author']
    books_date = request.form['books_date']
    books_category = request.form['books_category']
    books_position = request.form['books_position']
    books_status = request.form['books_status']
    books_review = request.form['books_review']
    books_image = request.form['books_image']

    if books_name and books_author and books_date and books_category and books_position and books_review and books_image:
        cursor = db.database.cursor()
        sql = "INSERT INTO books (books_name, books_author, books_date, books_category, books_position, books_status, books_review, books_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (books_name, books_author, books_date, books_category, books_position, books_status, books_review, books_image)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

## Ruta para borrar los libros a través de la tabla
@app.route('/delete/<string:books_id>')
def delete(books_id):
    cursor = db.database.cursor()
    sql = "DELETE FROM books WHERE books_id=%s"
    data = (books_id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

## Ruta para editar los libros a través de la tabla
@app.route('/edit/<string:books_id>', methods=['POST'])
def edit(books_id):
    books_id = request.form['books_id']
    books_name = request.form['books_name']
    books_author = request.form['books_author']
    books_date = request.form['books_date']
    books_category = request.form['books_category']
    books_position = request.form['books_position']
    books_status = request.form['books_status']
    books_review = request.form['books_review']
    books_image = request.form['books_image']

    if books_name and books_author and books_date and books_category and books_position and books_review and books_image:
        cursor = db.database.cursor()
        sql = "UPDATE books SET books_name = %s, books_author = %s, books_date = %s, books_category = %s, books_position = %s, books_status = %s, books_review = %s, books_image = %s WHERE books_id = %s"
        data = (books_name, books_author, books_date, books_category, books_position, books_status, books_review, books_image, books_id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)