#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import total_ordering


@total_ordering
class TokenProperty:
    """A TokenProperty represents a property of a token.

    E.g. the 'Word' or 'PoS-Tag' property. A Token then maps such properties to
    property values, such as "house" or "NN". Each TokenProperty has a name (say
    'Word') and an integer 'level' that can be used to define an order on
    properties. This order is for example used when the properties of a token
    are stacked under each other in the graphical representation of a token.

    Attributes:
        name (str): The name of the property.
        level (int): The level of the property.
    """

    
    def __init__(self, name: str=None, level: int=0):
        """Create a new property.

        Args:
            name (str, optional): The name of the property. If not given then it is set to
                'Property <level>' where <level> is the level of the created property.
            level (int, optional): The level of the property. Defaults to 0.
        """
        name = name if name is not None else "Property {0}".format(level)
        self.name = name
        self.level = level


    def __eq__(self, other):
        """Two TokenProperty objects are equal iff their names match.

        Args:
            other (TokenProperty): The other property.

        Returns:
            bool: True iff the property names are equal.
        """
        return self.name == other.name


    def __ne__(self, other):
        """Two TokenProperty objects are not equal iff their names are different.

        Args:
            other (TokenProperty): The other property.
 
        Returns:
            bool: True iff the property names are not equal.
        """
        return self.name != other.name

    
    def __lt__(self, other):
        """First compares the level of the two properties and if these are equal the
        property names are compared.

        Args:
            other (TokenProperty): The other property.
 
        Returns:
            bool: True iff the tokens level is less than the other token's level, or
            the levels are identical but the token's name is lexicographically smaller
            than the other.
        """
        return self.level < other.level or (self.level == other.level and
                                            self.name < other.name)


    def __hash__(self):
        """Calculates a hashcode based on the property name.

        Returns:
            int: A hashcode based on the property name. 
        """
        return hash(self.name) if self.name is not None else 0

