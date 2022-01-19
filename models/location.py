# A Class is like an object constructor, or a "blueprint" for creating objects.

class Location():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        
        