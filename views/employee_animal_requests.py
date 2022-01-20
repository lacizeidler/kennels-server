import json
import sqlite3
from models.animal import Animal
from models.employee import Employee

from models.employee_animal import EmployeeAnimal


def get_all_employee_animals():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.employee_id,
            a.animal_id,
            l.name employee_name,
            l.address employee_address,
            l.location_id employee_location_id,
            b.name animal_name,
            b.status animal_status,
            b.breed animal_breed,
            b.customer_id animal_customer_id,
            b.location_id animal_location_id
        FROM EmployeeAnimals a
        JOIN Employee l
            ON l.id = a.employee_id
        JOIN Animal b
            ON b.id = a.animal_id
        """)

        employee_animals = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            employee_animal = EmployeeAnimal(
                row['id'], row['employee_id'], row['animal_id'])

            employee = Employee(row['id'], row['employee_name'],
                                row['employee_address'], row['employee_location_id'])

            animal = Animal(row['id'], row['animal_name'], row['animal_status'],
                            row['animal_breed'], row['animal_customer_id'], row['animal_location_id'])

            employee_animal.employee = employee.__dict__
            employee_animal.animal = animal.__dict__

            employee_animals.append(employee_animal.__dict__)

        return json.dumps(employee_animals)


def get_single_employee_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.employee_id,
            a.animal_id,
            l.name employee_name,
            l.address employee_address,
            l.location_id employee_location_id,
            b.name animal_name,
            b.status animal_status,
            b.breed animal_breed,
            b.customer_id animal_customer_id,
            b.location_id animal_location_id
        FROM EmployeeAnimals a
        JOIN Employee l
            ON l.id = a.employee_id
        JOIN Animal b
            ON b.id = a.animal_id
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        employee_animal = EmployeeAnimal(
            data['id'], data['employee_id'], data['animal_id'])

        employee = Employee(data['id'], data['employee_name'],
                            data['employee_address'], data['employee_location_id'])

        animal = Animal(data['id'], data['animal_name'], data['animal_status'],
                        data['animal_breed'], data['animal_customer_id'], data['animal_location_id'])

        employee_animal.employee = employee.__dict__
        employee_animal.animal = animal.__dict__

        return json.dumps(employee_animal.__dict__)
