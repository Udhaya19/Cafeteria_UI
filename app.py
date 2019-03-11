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
        return render_template('beverage_type.html', item=user_data['employeeid'])


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


@app.route('/list_hot_item', methods=['POST'])
def item_list():
    return hot_item(connection, request.form)


def hot_item(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = display_hot_available_items()
    items = []
    for row in rows:
        items.append({"id": row[0], "name": row[1]})
    return render_template("jinja_hot_item.html", items=items, empid=array_value)


def display_hot_available_items():
    cursor = connection.cursor()
    cursor.execute("select item_id,item_name from beverages where availability='1' AND vendor_id=54321")
    record = cursor.fetchall()
    return record


@app.route('/list_cold_item', methods=['POST'])
def item_value():
    return cold_item(connection, request.form)


def cold_item(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = display_cold_available_items()
    item = []
    for row in rows:
        item.append({"id": row[0], "name": row[1]})
    return render_template("jinja_cold_item.html", items=item, empid=array_value)


def display_cold_available_items():
    cursor = connection.cursor()
    cursor.execute("select  item_id,item_name from beverages where availability  ='1' AND vendor_id=12345")
    record = cursor.fetchall()
    return record


@app.route('/cold_item', methods=['POST'])
def update_items():
    rows = updates(connection, request.form)
    return render_template('front_page.html', item=rows)


def updates(connection, user_data):
    item_values = list(user_data.values())
    employee_id = item_values[0]
    item_values.remove(item_values[0])
    item_key = list(user_data.keys())
    item_key.remove(item_key[0])
    for id in list(item_key):
        quantity = user_data[id]
        if int(quantity) != 0:
            cursor = connection.cursor()
            update_details = "insert into cart_details(employee_id,quantity,item_id) select {},{},item_id from beverages where item_id= {}".format(
                employee_id, quantity, id)
            cursor.execute(update_details)
            connection.commit()
            cursor.close()
        else:
            continue


@app.route('/hot_item', methods=['POST'])
def update_item():
    rows = update(connection, request.form)
    return render_template('front_page.html', item=rows)


def update(connection, user_data):
    item_values = list(user_data.values())
    employee_id = item_values[0]
    item_values.remove(item_values[0])
    item_key = list(user_data.keys())
    item_key.remove(item_key[0])
    for id in list(item_key):
        quantity = user_data[id]
        if int(quantity) != 0:
            cursor = connection.cursor()
            update_details = "insert into cart_details(employee_id,quantity,item_id) select {},{},item_id from beverages where item_id= {}".format(
                employee_id, quantity, id)
            cursor.execute(update_details)
            connection.commit()
            cursor.close()
        else:
            continue


@app.route('/report_generation', methods=['POST'])
def report_calculation():
    report_table = get_data_details(connection, request.form)
    totalcost = cost_calculation(connection, request.form)
    cost = totalcost[0]
    return render_template("display_report.html", item=cost, items=report_table)


def get_data_details(connection, user_data):
    cursor = connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    sql_update = "select cart_details.employee_id,beverages.item_id,beverages.item_name,cart_details.date,sum(cart_details.quantity*beverages.cost) " \
                 "FROM cart_details inner join beverages on cart_details.item_id=beverages.item_id  " \
                 "where beverages.vendor_id = %(vendor_id)s GROUP BY cart_details.employee_id,beverages.item_id,cart_details.date " \
                 "ORDER BY cart_details.employee_id"
    cursor.execute(sql_update, {'vendor_id': array_value})
    report_table = cursor.fetchall()
    cursor.close()
    return report_table


def cost_calculation(connection, user_data):
    cursor = connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    sql_query = "select sum(quantity*cost) from beverages inner join cart_details " \
                "on beverages.item_id = cart_details.item_id where vendor_id = %(vendor_id)s"
    cursor.execute(sql_query, {'vendor_id': array_value})
    totalcost = cursor.fetchall()
    cursor.close()
    return totalcost


if __name__ == '__main__':
    app.run()
