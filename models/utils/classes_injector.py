#!/usr/bin/python3
"""A classes injector for the defined models"""


class ClassesInjector:
    """Register classes once and inject them every where"""

    def __init__(self):
        """Initialize the injector"""
        self._classes = {}

    def register(self, *args, **kwargs):
        """Register a new class

        Example:
            >>> injector.register(Class1, MyClass=Class2, Class3)"""
        for cls in args:
            self._classes[cls.__name__] = cls
        for k, v in kwargs.items():
            self._classes[k] = v

    @property
    def classes(self):
        """Returns a copy of the registered classes

        Returns: dict"""
        return self._classes.copy()

    @property
    def keys(self):
        """Return classes keys

        Returns: List"""
        return self._classes.keys()

    def hasClass(self, name):
        """Check if class is registered

        Args:
            name (str): class name

        Returns: bool"""
        if type(name) is not str:
            raise TypeError('name must be a string')
        return name in self._classes

    def __getitem__(self, name):
        """Return a class by name """
        return self._classes[name]

    def __setitem__(self, name, value):
        """Set a class by name """
        self._classes[name] = value
