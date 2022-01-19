# The __init__.py file makes Python treat directories containing it as modules. Furthermore, this is the first file to be loaded in a module, so you can use it to execute code that you want to run each time a module is loaded, or specify the submodules to be exported.

from .animal_requests import (create_animal, delete_animal, get_all_animals,
                              get_single_animal, update_animal)
from .customers_requests import (create_customer, delete_customer,
                                 get_all_customers, get_single_customer,
                                 update_customer, get_customers_by_email)
from .employees_requests import (create_employee, delete_employee,
                                 get_all_employees, get_single_employee,
                                 update_employee)
from .locations_requests import (create_location, delete_location,
                                 get_all_locations, get_single_location,
                                 update_location)
