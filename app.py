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


# @app.route('/cold_beverage')
# def cold_beverage():
#     return render_template('cart_list_coldbeverage.html')
#
#
# @app.route('/hot_beverage')
# def hot_beverage():
#     return render_template('cart_list_hotbeverage.html')


@app.route('/vendorloginpage')
def vendor_login():
    return render_template('vendor_type.html')


@app.route('/juice_world')
def jw_login():
    return render_template("vendor_login.html", name='12345')


@app.route('/madras_cafe')
def mc_login():
    return render_template("vendor_login.html", name='54321')


@app.route('/vendor_operation', methods=['POST'])
def vendor_operation():
    return validate_vendor(connection, request.form)


def validate_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute(
        "select vendor_id,vendor_password from vendor_login where (vendor_id=%(vendor_id)s AND vendor_password=%(vendor_password)s)",
        {'vendor_id': user_data['id'], 'vendor_password': user_data['psw']}, )
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return render_template('vendor_login.html')
    else:
        return render_template('vendor_operation.html', vendorname=user_data['vendorname'])


@app.route('/availablity')
def cold():
    rows = database_connection_cold(connection, request.query_string)
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("home_page.html", items=items)


def database_connection_cold(connection, user_data):
    cursor = connection.cursor()
    query = "select item_name from beverage_type_details where reference_id = %s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
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


@app.route('/hot_beverage')
def hot_item():
    rows = display_available_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("display_availability.html", items=items)


def display_available_items():
    cursor = connection.cursor()
    cursor.execute("select item_name from beverage_type_details where availability='yes'")
    record = cursor.fetchall()
    return record


@app.route('/list_hot_item')
def list_hot_item():
    return render_template("menu.html")

#
# @app.route('/cold_beverage')
# def cold_item():
#     rows = display_available_items()
#     items = []
#     for row in rows:
#         items.append(row[0])
#     return render_template("display_availability.html", items=items)
#
#
# def display_available_items():
#     cursor = connection.cursor()
#     cursor.execute("select item_name from beverage_type_details where availability='yes'")
#     record = cursor.fetchall()
#     return record
#



if __name__ == '__main__':
    app.run()
