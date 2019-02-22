import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=thoughtworks_cafeteria user=admin")


@app.route('/')
def home():
    return render_template('front_page.html')


@app.route('/employeeloginpage')
def employee_login():
    return render_template('employee_id.html')


def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into employee_login_details(employee_id) values(%s);""",
                   (user_data['employeeid'],))
    connection.commit()
    cursor.close()


def validate_employee(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id=%(emp_id)s",
                   {'emp_id': user_data['employeeid']})
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return render_template('employee_id.html')
    else:
        post_data(connection, user_data)
        return render_template('beverage_type.html')


@app.route('/beverage', methods=['POST'])
def beverage_type():
    return validate_employee(connection, request.form)


@app.route('/cold_beverage')
def cold_beverage():
    return render_template('cart_list_coldbeverage.html')


@app.route('/hot_beverage')
def hot_beverage():
    return render_template('cart_list_hotbeverage.html')


@app.route('/vendorloginpage')
def vendor_login():
    return render_template('vendor_login.html')


def validate_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_name,vendor_password from vendor_login where vendor_name=%(id)s,vendor_password=%(password)s",
                   {'id': user_data['employeeid'],'password':user_data['']})
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return render_template('vendor_login.html')
    else:
        post_data(connection, user_data)
        return render_template('report_page.html')


if __name__ == '__main__':
    app.run()
