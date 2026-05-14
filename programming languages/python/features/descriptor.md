# Descriptor

descriptor in python is implemented in C which brings efficiency

https://www.youtube.com/watch?v=Fot3_9eDmOs&list=PLC0nd42SBTaMpVAAHCAifm5gN2zLk2MBo&index=17

By using descriptors, you can define custom behavior for attribute access on your classes. This allows you to control how attributes are accessed, modified, or deleted, providing a powerful mechanism for managing and validating data.
Here's a simple example of a descriptor that performs type checking:

"""python
class TypeCheckDescriptor:
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type
    
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if not isinstance(value, self.data_type):
            raise ValueError(f"Invalid type. Expected {self.data_type.__name__}.")
        instance.__dict__[self.name] = value

class MyClass:
    attribute = TypeCheckDescriptor('attribute', int)

obj = MyClass()
obj.attribute = 42  # Assigning a valid integer value
print(obj.attribute)  # Accessing the attribute
obj.attribute = "invalid"  # Assigning an invalid value (raises ValueError)
"""

