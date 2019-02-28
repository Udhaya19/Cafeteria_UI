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
    return render_template('vendor_type.html')


@app.route('/juice_world')
def jw_login():
    return render_template("vendor_login.html")


@app.route('/madras_cafe')
def mc_login():
    return render_template("vendor_login.html")


@app.route('/vendor_operation', methods=['POST'])
def vendor_operation():
    return validate_vendor(connection, request.form)


def validate_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id from vendor_login where vendor_id=%(vendor_id)s",
                   {'vendor_id': user_data['id']})

    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return render_template('vendor_login.html')
    else:
        return render_template('vendor_operation.html')


@app.route('/availablity')
def cold():
    rows = database_connection_cold()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("home_page.html", items=items)


def database_connection_cold():
    cursor = connection.cursor()
    cursor.execute("select  item_name from beverage_type_details where reference_id= '54321'")
    record = cursor.fetchall()
    return record


@app.route('/submission', methods=['POST'])
def menu_list_cold():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_query = "update  beverage_type_details set availability = 'no'"
    sql = "update beverage_type_details set availability = 'yes' where item_name IN %s"
    cursor.execute(sql_query)
    cursor.execute(sql, (array,))
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    app.run()
