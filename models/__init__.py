# The __init__.py file makes Python treat directories containing it as modules. Furthermore, this is the first file to be loaded in a module, so you can use it to execute code that you want to run each time a module is loaded, or specify the submodules to be exported.

from .animal import Animal
from .employee import Employee
from .customer import Customer
from .location import Location
from .employee_animal import EmployeeAnimal
