import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS
from modules.post_details_to_databse import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=thoughtworks_cafeteria user=admin")


@app.route('/')
def home():
    return render_template('front_page.html')


@app.route('/employeeloginpage')
def employee_login():
    return render_template('employee_id.html')


def validate_employee(connection, user_data):
    cursor = connection.cursor()
    result = cursor.execute("""select employee_id from employee_details where employee_id = %s ;""",
                            (user_data['employeeid'],))
    connection.commit()
    cursor.close()
    if result == user_data['employeeid']:
        return render_template('beverage_type.html')
    else:
        return render_template('employee_id.html')

@app.route('/beverage', methods=['POST'])
def beverage_type():
    post_data(connection, request.form)
    return render_template('beverage_type.html', shared=request.form)
@app.route('/vendorloginpage')
def vendor_login():
    return render_template('vendor_login.html')



if __name__ == '__main__':
    app.run()
