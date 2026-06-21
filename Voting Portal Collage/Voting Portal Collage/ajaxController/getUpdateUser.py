from  flask import jsonify

def get_active_users(db_connection):
    userList = []
    try:
        cursor = db_connection.cursor()
        query = '''SELECT u.user_id,first_name,last_name,email,contact_no,role_description,u.status FROM vote.users u, vote.user_role ur, vote.roles r 
                    WHERE u.status in( 'ACTV','INAC')
                    and u.user_id = ur.user_id
                    and ur.role_id = r.role_id
                    and r.role_code <>'ADMIN'
                    '''
        cursor.execute(query)
        userList = cursor.fetchall()
        return userList
    except Exception as e:
        print(f"Error fetching active users: {e}")
        return 500
    finally:
        cursor.close()
        db_connection.close()

def update_user_fields(db_connection, user_id, fields):
    status = 400
    try:
        cursor = db_connection.cursor()
        
        # Update user fields
        user_fields = {k: v for k, v in fields.items() if k != 'role'}
        if user_fields:
            set_clause = ", ".join([f"{field} = %s" for field in user_fields.keys()])
            values = list(user_fields.values())
            values.append(user_id)
            query = f"UPDATE vote.users SET {set_clause} WHERE user_id = %s"
            cursor.execute(query, values)
        
        # Update user role if 'role' is provided
        if 'role' in fields:
            query = "UPDATE vote.user_role SET role_id = (select role_id from vote.roles where role_code=%s) WHERE user_id = %s"
            cursor.execute(query, (fields['role'], user_id))
        
        db_connection.commit()
        
        if cursor.rowcount > 0:
            status = 200
        else:
            status = 400
    except Exception as e:
        print(f"Error updating user fields: {e}")
        db_connection.rollback()
        return jsonify({"statusCode": 500, "error": str(e)})
    finally:
        cursor.close()
        db_connection.close()
        return jsonify({"statusCode": status})

def create_users(db_connection, users):
    status = 400
    try:
        cursor = db_connection.cursor()
        user_query = """
        INSERT INTO vote.users (first_name, last_name, email, contact_no, password, status,prn_no)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
        RETURNING user_id
        """
        role_query = """
        INSERT INTO vote.user_role (user_id, role_id)
        VALUES (%s, (SELECT role_id FROM vote.roles WHERE role_code = %s))
        """
        
        for user in users:
            user_data = user[:-1]  # All values except the last one (role_id)
            role_id = user[-1]  # The last value (role_id)
            
            cursor.execute(user_query, user_data)
            user_id = cursor.fetchone()[0]
            
            cursor.execute(role_query, (user_id, role_id))
        
        db_connection.commit()
        if cursor.rowcount > 0:
            status = 200
        else:
            status = 400
    except Exception as e:
        print(f"Error creating users: {e}")
        db_connection.rollback()
        return jsonify({"statusCode": 500, "error": str(e)})
    finally:
        cursor.close()
        db_connection.close()
        return jsonify({"statusCode": status})
