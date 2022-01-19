import json
import sqlite3

from models.location import Location


LOCATIONS = [
    {
        "id": 1,
        "name": "Chicago",
        "status": "Active"
    },
    {
        "id": 2,
        "name": "Nashville",
        "status": "Active"
    },
    {
        "id": 3,
        "name": "San Diego",
        "status": "Active"
    }
]


def get_all_locations():
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
            a.address
        FROM location a
        """)

        # Initialize an empty list to hold all customer representations
        locations = []

        # Convert rows of data into a Python list
        # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples.
        # Tuples are used to store multiple items in a single variable.
        # mytuple = ("apple", "banana", "cherry")
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # location class above.
            location = Location(row['id'],
                                row['name'],
                                row['address'])

            locations.append(location.__dict__)

    # Use `json` package to properly serialize list as JSON
    # json.dumps() function converts a Python object into a json string.
    return json.dumps(locations)


# Function with a single parameter
def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        location = Location(data['id'], data['name'],
                            data['address'])

        return json.dumps(location.__dict__)


def create_location(location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Location
            (name, address)
        VALUES  
            (?,?);
        """, (location['name'], location['address']))

        id = db_cursor.lastrowid

        location['id'] = id

    return json.dumps(location)


def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
# This method accepts a MySQL query as a parameter and executes the given query.
        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))


def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['name'], new_location['address'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
