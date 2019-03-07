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


def validate_employee(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select id from employee_details where id=%(emp_id)s",
                   {'emp_id': user_data['employeeid']})
    result = cursor.fetchall()

    cursor.close()
    if len(result) == 0:
        return render_template('employee_id.html')
    else:
        return render_template('beverage_type.html')


@app.route('/beverage', methods=['POST'])
def beverage_type():
    return validate_employee(connection, request.form)


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
        "select id,password from vendor_login where (id=%(vendor_id)s AND password=%(vendor_password)s)",
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
    value = (int(request.query_string.decode().split('=')[1]),)
    list1 = list(value)
    index = list1[0]
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_display_available.html", items=items, name=index)


def database_connection_cold(connection, user_data):
    cursor = connection.cursor()
    query = "select item_name from beverages where vendor_id = %s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
    record = cursor.fetchall()
    return record


@app.route('/submission', methods=['POST'])
def menu_list_cold():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    sql_update = "update beverages set availability = '0' where vendor_id=%(vendor_id)s"
    sql_data = "update beverages set availability = '1' WHERE item_name  IN %s"
    cursor.execute(sql_update, {'vendor_id': array_value})
    cursor.execute(sql_data, (array,))
    connection.commit()
    cursor.close()


@app.route('/list_hot_item')
def hot_item():
    rows = display_hot_available_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_hot_item.html", items=items)


def display_hot_available_items():
    cursor = connection.cursor()
    cursor.execute("select item_name from beverages where availability='1' AND vendor_id=54321")
    record = cursor.fetchall()
    return record


@app.route('/list_cold_item')
def cold_items():
    rows = display_cold_available_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_cold_item.html", items=items)


def display_cold_available_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from beverages where availability  ='1' AND vendor_id=12345")
    record = cursor.fetchall()
    return record


@app.route('/cold_item')
def list_cold_item():
    return render_template("last_page.html")


@app.route('/hot_item', methods=['POST'])
def update_item():
    return update(connection, request.form)


def update(connection, update_data):
    item = update_data.to_dict()
    a = []
    b = []
    i = 0
    j = 1
    for row in range(len(item)):
        a.append(list(item.keys())[i])
        b.append(list(item.values())[j])

        cursor = connection.cursor()
        update_details = "insert into cart_details (item_id,quantity) select item_id, {} from beverages where item_name = '{}'".format(
            b[0], a[0])
        cursor.execute(update_details)
        connection.commit()
        cursor.close()
        i += 2
        j += 2
    return update_details


if __name__ == '__main__':
    app.run()
