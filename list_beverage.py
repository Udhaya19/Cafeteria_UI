import psycopg2
from flask import Flask,request,render_template
import json
app = Flask(__name__)


@app.route('/')
def hello():
    is_valid = database_connect()
    print(is_valid)
    return json.dumps(is_valid)


def database_connect():

    try:
        print("try is running")
        connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                                      database="thoughtworks_cafeteria")
        cursor = connection.cursor()
        cursor.execute("select hot_item_name from hot_beverage")

        record = cursor.fetchall()

        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


hello()
database_connect()
if __name__ == '__main__':
    app.run()
