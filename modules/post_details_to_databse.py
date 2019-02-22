def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""SELECT * INTO thoughtworks_cafeteria FROM employee_details WHERE employee_id==employeeid;
                        IF NOT FOUND THEN 
                        RAISE EXCEPTION 'employee % not found',employeeid
                        END IF;""",
                   (user_data['employeeid']))
    connection.commit()
    cursor.close()
