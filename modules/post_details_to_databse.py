def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into employee_details(employee_id) values(%s);""",
                   (user_data['employeeid'],))
    connection.commit()
    cursor.close()
