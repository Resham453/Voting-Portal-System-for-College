import psycopg2
from psycopg2.extras import RealDictCursor

# Connect to the database 
def get_connection():
    conn = psycopg2.connect(
        database="voting_portal", user="postgres", 
        password="Resham@453", host="localhost", port="5432"
    )
    return conn

# Function to execute a query and return the result
def execute_query(query, params=None):
    conn = None
    result = None
    try:
        # Get the connection
        conn = get_connection()

        # Create a cursor
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Execute the query (with optional parameters)
        cur.execute(query, params)

        # If the query is a SELECT, fetch all rows
        if query.strip().upper().startswith("SELECT"):
            result = cur.fetchall()
        else:
            # If it's an insert, update, or delete, commit the changes
            conn.commit()

        # Close the cursor
        cur.close()

    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if conn is not None:
            conn.close()

    return result

def execute_normal_query(query,param=None):

    conn = None
    result = None
    try:
        # Get the connection
        conn = get_connection()

        # Create a cursor
        cur = conn.cursor()

        # Execute the query (with optional parameters)
        cur.execute(query)

        # If the query is a SELECT, fetch all rows
        if query.strip().upper().startswith("SELECT"):
            result = cur.fetchall()
        else:
            # If it's an insert, update, or delete, commit the changes
            conn.commit()

        # Close the cursor
        cur.close()

    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if conn is not None:
            conn.close()

    return result

if __name__ == "__main__":
    # Example usage
    query ="select * from  vote.users "
    params = ("admin@gmail.com",)
    users = execute_query(query)
    print(users)  # This will print the fetched data as a list of dictionaries
    print(users[0])

    # # For a non-SELECT query (e.g., INSERT/UPDATE)
    # query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    # params = ("New User", "new_user@example.com")
    # execute_query(query, params)  # This will insert a new user into the database
