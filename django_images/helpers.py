def classproperty(func):
    """Method decorator to turn a method into a class property.

    Only getting the value is possible"""

    class _classproperty(property):

        def __get__(self, cls, owner):
            return self.fget.__get__(None, owner)()

    return _classproperty(classmethod(func))
