import psycopg2
import sqlite3



def connect_to_database():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('dataBase/paitent.db')
        # Connect to PostgreSQL database
        # conn = psycopg2.connect(host='localhost', port='5432', dbname='braintumor', password='123456', user='postgres')
        # print("Database connected successfully")
        return conn
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None


def create_tables():
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS patient (
                name TEXT,
                age INT,
                gender TEXT,
                contact TEXT,
                filename TEXT,
                result FLOAT
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS doctor (
                filename TEXT,
                result FLOAT
            );
            """)
            conn.commit()
            # print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()

# Call create_tables function before performing any other operations
create_tables()


def get_patient_data():
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patient;")
            data = cur.fetchall()  # Fetch all rows
            return data
        except Exception as e:
            print(f"Error retrieving patient data: {e}")
        finally:
            conn.close()
    return []

def add_patient_data(name, age, gender, contact, filename, result):
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            query = """
            INSERT INTO patient(name, age, gender, contact, filename, result)
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM patient WHERE name = ? AND age = ? AND gender = ?
            );
            """
            values = (name, age, gender, contact, filename, result, name, age, gender)
            cur.execute(query, values)
            conn.commit()
            print("Patient data inserted successfully")
        except Exception as e:
            print(f"Error inserting patient data: {e}")
        finally:
            conn.close()

def get_doctor_data():
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctor;")
            data = cur.fetchall()  # Fetch all rows
            return data
        except Exception as e:
            print(f"Error retrieving doctor data: {e}")
        finally:
            conn.close()
    return []

def add_doctor_data(filename, result):
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            query = """
            INSERT INTO doctor(filename, result)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM doctor WHERE filename = ? AND result = ?
            );
            """
            values = (filename, result, filename, result)
            cur.execute(query, values)
            conn.commit()
            print("Doctor data inserted successfully")
        except Exception as e:
            print(f"Error inserting doctor data: {e}")
        finally:
            conn.close()

# Example usage
# add_patient_data(name="mohit", age=20, gender='male', contact=76, filename='gaurav.jpg', result=9.999)
# add_doctor_data('2.jpg',2.14)
# print(get_patient_data())
# print(get_doctor_data())
