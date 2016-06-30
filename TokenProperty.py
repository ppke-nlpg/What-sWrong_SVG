class TokenProperty(object):
    # The name of the property.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # The level of the property.
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    # Creates a property with the given name and level 0.

    # @param name the name of the property.
    def __init__(self, name=None, level=None):
        if name is not None:
            self._name = name
            if level is not None:
                self._level = level
            else:
                self._level = 0
        else:
            if level is not None:
                self._level = level
                self._name = "Property " + level

    # Returns the name of the property.

    # @return the name of the property.
    def __str__(self):
        return self._name

    # Two TokenProperty objects are equal iff their names match.

    # @param o the other property.
    # @return true iff the property names match.

    def __eq__(self, other):
#        if other == self:
 #           return True
        if other is None or type(other) != type(self):
            return False

        if self._name is not None:
            if self._name != other.name:
                return False
        else:
            if other.name is not None:
                return False
        return True

    # Calculates a hashcode based on the property name.

    # @return a hashcode based on the property name.
    def __hash__(self):
        if self._name is not None:
            return hash(self._name)
        else:
            return 0

    # First compares the level of the two properties and if these are equal the property names are compared.

    # @param o the other property.
    # @return a value larger than 0 if this level is larger than the other level or the levels equal and this name is
    #         lexicographically larger than the other. A value smaller than 0 is returned if this level is smaller than
    #         the other level or the levels equal and this name is lexicographically smaller than the other. Otherwise 0
    #         is returned.
    def compareTo(self, other):
        if self._level != other.level:
            return self._level - other.level
        else:
            if self._name > other.name:
                return 1
            else:
                return -1
            # return self._name.compareTo(other.name) TODO: Ez így nem lesz jó
