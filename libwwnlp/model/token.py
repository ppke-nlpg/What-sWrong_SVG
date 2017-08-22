#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import re # This was only needed for the commented out part in the propvals_contain method


class Token:
    """A Token represents a word in an utterance.

    It consists of an index and a set of properties with their value.

    Attributes:
        index (int): The index of the token.
        token_properties (Dict[TokenProperty, Object]): A mapping from
            properties to values.
    """

    def __init__(self, index: int):
        """Creates a new token with the given index and actuality value.

        Args:
            index (int): The index of the token.
        """
        self.index = index
        self.token_properties = {}

    def get_property(self, name: str) -> str:
        """Get the value of the given property.

        Args:
            name (str): The property name to get the value for.

        Returns:
            The value of the given property.
        """
        if name in self.token_properties:
            return self.token_properties[name][1]

    def remove_property(self, name: str):
        """Remove the property value with the given name.

        Args:
            name (str): The name of the property to remove.
        """
        del self.token_properties[name]
        return self

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

    def get_sorted_properties(self) -> tuple:
        """Return a list of sorted token properties.

        Returns:
            tuple: The list of sorted token properties.
        """
        return tuple(name for lvl, name in sorted((lvl, name) for name, (lvl, _) in self.token_properties.items()))

    def propvals_contain(self, substrings: set, whole_word: bool=False) -> bool:
        """Check whether any of the property values contains the given strings.

        Args:
            substrings (set): Set of strings to check.
            whole_word (bool, optional): Should we check for complete words or
                is it enough for the given strings to be substrings of the
                token value. Defaults to False.

        Returns:
            bool: True iff there is a property value that is equal to/contains
            one of the strings in `substrings`.
        """
        for _, curr_prop_val in self.token_properties.values():
            for substr in substrings:
                # TODO: Do this properly...
                # if re.match("\d+-\d+$", substr):  # Full string match in JAVA!
                #     start, end = substr.split("-")
                #     if int(start) <= int(curr_prop_val) <= int(end):
                #         return True
                if curr_prop_val == substr or (not whole_word and substr in curr_prop_val):
                    return True
        return False

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
        return "{0}:{1}".format(self.index, ", ".join(str(prop) for prop in self.token_properties))
