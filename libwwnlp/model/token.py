#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Token:
    """A Token represents a word in an utterance.

    It consists of an index and a set of properties with their value.

    Attributes:
        index (int): The index of the token.
        token_properties (Dict[TokenProperty, Object]): A mapping from properties to values.
    """

    def __init__(self, index: int):
        """Creates a new token with the given index and actuality value.

        Args:
            index (int): The index of the token.
        """
        self.index = index
        self.token_properties = {}

    def add_property(self, name: str, value: str, level=None):
        """Add a property with the given name and value.

        Args:
            name (str): The name of the property to be added.
            value (str): The value of the property to be added.
            level (int, optional): The level of the property to be added. If
                not given it will be set to the number of the token's
                properties (prior to the ongoing addition).

        Returns:
            Token: The token itself.
        """
        level = level if level is not None else len(self.token_properties)
        self.token_properties[name] = (level, value)
        return self

    def remove_property(self, name: str):
        """Remove the property value with the given name.

        Args:
            name (str): The name of the property to remove.
        """
        del self.token_properties[name]
        return self

    def get_property_names(self) -> tuple:
        """Return a list of sorted token properties.

        Returns:
            tuple: The list of sorted token properties.
        """
        return tuple(name for lvl, name in sorted((lvl, name) for name, (lvl, _) in self.token_properties.items()))

    def get_property_value(self, name: str) -> str:
        """Get the value of the given property.

        Args:
            name (str): The property name to get the value for.

        Returns:
            The value of the given property.
        """
        if name in self.token_properties:
            return self.token_properties[name][1]

    def merge(self, token, forbidden_token_properties: set=None):
        """Inserts all properties and values of the other token into this token.

        In case of clashes the value of the other token is taken.

        Args:
            token (Token): The token to merge with.
            forbidden_token_properties (Set[TokenProperty]): Properites not to
                merge as they are forbidden.
        """
        for curr_prop_name, (lvl, value) in token.token_properties.items():
            if forbidden_token_properties is None or curr_prop_name not in forbidden_token_properties:
                self.token_properties[curr_prop_name] = (lvl, value)

    def __eq__(self, other):
        """Checks whether the two tokens have the same index.

        Note:
            Hence equality is only defined through the position of the token in
            the sentence.

        Args:
            other (Token): The other token.

        Returns:
            bool: True iff the two tokens have the same index.
        """
        return other is not None and isinstance(other, self.__class__) and self.index == other.index

    def __hash__(self):
        """Returns the index of the token as its hashcode.

        Returns:
            int: The index of the token.
        """
        return self.index

    def __str__(self):
        """Return a string representation of this token.

        Returns:
            str: A string representation of this token.
        """
        return '{0}:{1}'.format(self.index, ', '.join(str(prop) for prop in self.token_properties))
