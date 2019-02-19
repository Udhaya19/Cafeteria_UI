def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into student_details(student_id,student_name) values(%s, %s);""",
                   (user_data['id'], user_data['name']))
    connection.commit()
    cursor.close()
