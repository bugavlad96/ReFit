from flask_mysqldb import MySQL


def connect_db(app):
    # Configure MySQL
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '29122417'
    app.config['MYSQL_DB'] = 'refit'

    mysql = MySQL(app)

    return mysql
