import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
import anvil.server
import psycopg2  # Librería para interactuar con PostgreSQL

# Establecer la conexión a la base de datos PostgreSQL
def get_db_connection():
    """Crea y retorna una conexión a la base de datos PostgreSQL"""
    connection = psycopg2.connect(
        dbname="´public",  # Reemplaza con el nombre de tu base de datos
        user="postgres",      # Reemplaza con tu usuario de PostgreSQL
        password="catalina",  # Reemplaza con tu contraseña de PostgreSQL
        host="localhost",     # Reemplaza con el host de tu servidor PostgreSQL
        port="5432"           # Reemplaza con el puerto de tu servidor PostgreSQL si es diferente
    )
    return connection

@anvil.server.callable
def get_employees():
    """Obtener todos los empleados de la base de datos"""
    connection = get_db_connection()
    with connection.cursor() as cur:
        cur.execute("SELECT id, name, position, salary FROM employees")
        rows = cur.fetchall()
        employees = [{'id': r[0], 'name': r[1], 'position': r[2], 'salary': r[3]} for r in rows]
    connection.close()
    return employees

@anvil.server.callable
def add_employee(name, position, salary):
    """Agregar un nuevo empleado a la base de datos"""
    connection = get_db_connection()
    with connection.cursor() as cur:
        cur.execute("INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)",
                    (name, position, salary))
        connection.commit()
    connection.close()

@anvil.server.callable
def update_employee(emp_id, name, position, salary):
    """Actualizar información de un empleado existente"""
    connection = get_db_connection()
    with connection.cursor() as cur:
        cur.execute("UPDATE employees SET name=%s, position=%s, salary=%s WHERE id=%s",
                    (name, position, salary, emp_id))
        connection.commit()
    connection.close()

@anvil.server.callable
def delete_employee(emp_id):
    """Eliminar un empleado de la base de datos"""
    connection = get_db_connection()
    with connection.cursor() as cur:
        cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
        connection.commit()
    connection.close()