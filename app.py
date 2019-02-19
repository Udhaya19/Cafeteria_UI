import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

from modules.post_details_to_databse import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=student user=admin")


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/post-data', methods=['POST'])
def get_data():
    post_data(connection, request.form)
    return render_template('student_details.html', shared=request.form)


if __name__ == '__main__':
    app.run()
