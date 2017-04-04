#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .token_property import TokenProperty
#import re # This is only needed for the commented out part in properties_contain
from operator import attrgetter

class Token:
    """A Token represents a word in an utterance.

    It consists of an index and a set of properties with their value.

    Attributes:
        index (int): The index of the token.
        token_properties (Dict[TokenProperty, Object]): A mapping from properties
            to values.
        is_actual (bool): Whether the token is actually part of the analysis or
            only provides context (e.g. in the case of a partial analysis visualisation).
            Defaults to False.
    """

    
    def __init__(self, index: int, is_actual: bool=False):
        """Creates a new token with the given index and actuality value.
        
        Args:
            index (int): The index of the token.
            is_actual (bool, optional): Whether the token is actual. Defaults
                to False.
        """
        self.index = index
        self.token_properties = {}  
        self.is_actual = is_actual


    def get_property(self, token_property) -> str:
        """Get the value of the given property.

        Args:
            token_property (TokenProperty): The property to get the value for.

        Returns:
            The value of the given property.
        """
        return self.token_properties[token_property]

    
    def remove_property(self, name):
        """Remove the property value with the given name.

        Args:
            name (str): The name of the property to remove.
        """
        del self.token_properties[TokenProperty(name=name)]
        return self


    def add_property(self, token_property: TokenProperty, value: str):
        """Add a property with the given value.

        Args:
            token_property (TokenProperty): The property to be added.
            value (str): The value of the property to be added.

        Returns:
            Token: The token itself.
        """
        self.token_properties[token_property] = value
        return self

    
    def add_named_prop(self, name: str, value: str, level=None):
        """Add a property with the given name and value.

        Args:
            name (str): The name of the property to be added.
            value (str): The value of the property to be added.
            level (int, optional): The level of the property to be added.
                If not given it will be set to the number of the token's properties
                (prior to the ongoing addition).
        
        Returns:
            Token: The token itself.
        """
        level = level if level is not None else len(self.token_properties)
        self.token_properties[TokenProperty(name, level)] = value
        return self

    
    def getSortedProperties(self) -> list:
        """Return a list of sorted token properties.

        Returns:
            list: The list of sorted token properties.
        """
        sorted_properties = list(sorted(self.token_properties.keys(),
                                        key=attrgetter('level', 'name')))
        return sorted_properties


    def get_property_types(self):
        """Return all token properties.

        Note:
            To get the value of a property use Token#get_property(TokenProperty).
        
        Returns:
            tuple: A tuple containing the token's properties.
        """
        return tuple(self.token_properties.keys())

    
    def properties_contain(self, substrings: set, wholeWord: bool=False) -> bool:
        """Check whether any of the property values contains the given strings.
        
        Args:
            substrings (set): Set of strings to check.
            wholeWord (bool, optional): Should we check for complete words or is it enough
                for the given strings to be substrings of the token value. Defaults to False.

        Returns:
            bool: True iff there is a property value that is equal to/contains one of the
            strings in :substrings:.
        """
        for curr_property in self.token_properties.values():
            for substr in substrings:
                # if re.match("\d+-\d+$", substr):  # Full string match in JAVA!
                #     start, end = substr.split("-")
                #     if int(start) <= int(curr_property) <= int(end):
                #         return True
                if curr_property == substr or (not wholeWord and substr in curr_property):
                    return True
        return False

    
    def merge(self, token):
        """Inserts all properties and values of the other token into this token.

        In case of clashes the value of the other token is taken.

        Args:
            token (Token): The token to merge with.
        """
        self.token_properties.update(token.token_properties)

        
    def __eq__(self, other):
        """Checks whether the two tokens have the same index.

        Note:
            Hence equality is only defined through the position of the token in the sentence. 

        Args:
            other (Token): The other token.
        
        Returns:
            bool: True iff the two tokens have the same index.
        """
        return (other is not None and isinstance(other, self.__class__) and
                self.index == other.index)

        
    def __hash__(self):
        """Returns the index of the token as its hashcode.

        Returns:
            int: The index of the token.
        """
        return self.index

        
    def __str__(self):
        """Return a string representation of this token containing token index and properties.

        Returns:
            str: A string representation of this token.
        """
        return "{0}:{1}".format(self.index, ", ".join(str(prop)
                                                      for prop in self.token_properties))
