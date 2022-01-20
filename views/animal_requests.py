import json
import sqlite3

from models import Animal
from models.customer import Customer
from models.location import Location


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        # This method accepts a MySQL query as a parameter and executes the given query.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples.
        # Tuples are used to store multiple items in a single variable.
        # mytuple = ("apple", "banana", "cherry")
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['location_id'], row['customer_id'])

            # Create a Location instance from the current row
            location = Location(
                row['id'], row['location_name'], row['location_address'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    # Use `json` package to properly serialize list as JSON
    # json.dumps() function converts a Python object into a json string.
    return json.dumps(animals)

# Function with a single parameter


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            l.name customer_name,
            l.address customer_address,
            l.email customer_email,
            l.password customer_password,
            b.name location_name,
            b.address location_address
        FROM Animal a
        JOIN Customer l
            ON l.id = a.customer_id
        JOIN Location b
            ON b.id = a.location_id
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['status'], data['breed'],
                        data['customer_id'], data['location_id'])
        customer = Customer(data['id'], data['customer_name'], data['customer_address'],
                            data['customer_email'], data['customer_password'])
        location = Location(
            data['id'], data['location_name'], data['location_address'])

        animal.customer = customer.__dict__
        animal.location = location.__dict__

    return json.dumps(animal.__dict__)


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, status, breed, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['status'], new_animal['breed'],
               new_animal['customer_id'], new_animal['location_id']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return json.dumps(new_animal)


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
# This method accepts a MySQL query as a parameter and executes the given query.
        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                status = ?,
                breed = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['status'], new_animal['breed'],
              new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_animal_by_location_id(location_id):
    with sqlite3.connect(".kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.status,
            c.breed,
            c.customer_id,
            c.location_id
        from Animal c
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['status'], row['breed'],
                            row['customer_id'], ['location_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)
