#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

"""
 * A TokenProperty represents a property of a token, such as the 'Word' or "PoS-Tag' property. A {@link Token} then maps
 * such properties to property values, such as "house" or "NN". Each TokenProperty has a name (say 'Word') and an
 * integer 'level' that can be used to define an order on properties. This order is for example used when the properties
 * of a token are stacked under each other in the graphical representation of a token.
 *
 * @author Sebastian Riedel
"""


class TokenProperty:
    """
     * The name of the property.
    """
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    """
     * The level of the property.
    """
    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value

    """
     * Create new property with given name and level.
     *
     * @param name  the name of the property.
     * @param level the level of the property.
     
     OR
     
     * Creates a property with the given name and level 0.
     *
     * @param name the name of the property.
     
     OR
     
     * Creates a property with the given level and the name 'Property [level]' where [level] will be replaced with the
     * given level.
     *
     * @param level the level of the property.

    """
    def __init__(self, name: str=None, level: int=0):
        if name is None:
            name = "Property {0}".format(level)
        self._name = name
        self._level = level

    """
     * Returns the name of the property.
     *
     * @return the name of the property.
    """
    def __str__(self):
        return self._name
    """
     * Returns the name of the property.
     *
     * @return the name of the property.
    """
    # See the getter above...

    """
     * Returns the level of the property.
     *
     * @return the level of the property.
    """
    # See the getter above...

    """
     * Two TokenProperty objects are equal iff their names match.
     *
     * @param o the other property.
     * @return true iff the property names match.
    """
    def __eq__(self, other):
        return other is not None and isinstance(other, self.__class__) and\
               (self._name is None or self._name == other.name) and (self._name is not None or other.name is None)

    """
     * Calculates a hashcode based on the property name.
     *
     * @return a hashcode based on the property name.
    """
    def __hash__(self):
        if self._name is not None:
            return hash(self._name)
        else:
            return 0

    """
     * First compares the level of the two properties and if these are equal the property names are compared.
     *
     * @param o the other property.
     * @return a value larger than 0 if this level is larger than the other level or the levels equal and this name is
     *         lexicographically larger than the other. A value smaller than 0 is returned if this level is smaller than
     *         the other level or the levels equal and this name is lexicographically smaller than the other.
     *          Otherwise 0 is returned.
    """
    def compareTo(self, other):
        if self._level != other.level:
            return self._level - other.level
        else:
            if self._name > other.name:
                return 1
            elif self._name < other.name:
                return -1
            else:
                return 0
