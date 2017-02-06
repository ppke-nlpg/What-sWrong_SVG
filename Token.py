#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from TokenProperty import TokenProperty
import re
from operator import attrgetter


"""
 * A Token represents a word in an utterance. It consists of an index and a set of properties with name and value.
 *
 * @author Sebastian Riedel
"""


class Token:

    """
     * The index of the token.
    """
    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value

    """
     * A mapping from properties to values.
    """
    @property
    def tokenProperties(self):
        return self._tokenProperties

    @tokenProperties.setter
    def tokenProperties(self, value):
        self._tokenProperties = value

    """
     * Creates a new token with the given index.
     *
     * @param index the index of the token.
    """
    def __init__(self, index: int):
        self._index = index
        self._tokenProperties = {}  # HashMap<TokenProperty, String>()

    """
     * Returns the index of the token.
     *
     * @return the index of the token.
    """
    # See the getter above...
    """
     * Return all token properties (the property names). To get the value of a property use {@link
     * Token#getProperty(TokenProperty)}.
     *
     * @return a collection with token properties.
    """
    def getPropertyTypes(self):
        return tuple(self._tokenProperties.keys())

    """
     * Get the value of the given property.
     *
     * @param property the property to get the value for.
     * @return the value of the given property.
    """
    def getProperty(self, token_property) -> str:
        return self._tokenProperties[token_property]

    """
     * Remove the property value with given index.
     *
     * @param index the index of the property to remove.

    OR

     * Remove the property value with the given name.
     *
     * @param name the name of the property to remove.
    """
    def removeProperty(self, name: str=None, index: int=None):
        if index is not None:
            del self._tokenProperties[TokenProperty(name=name)]
        if name is not None:
            del self._tokenProperties[TokenProperty(level=index)]

    """
     * Add a property with the given name and value.
     *
     * @param name  the name of the property.
     * @param value the value of the property.
     * @return a pointer to this token.

    OR

     * Add the property with name "Property [index]" and the given value.
     *
     * @param index    the index of the property
     * @param property the value of the property.

    OR

     * Add a property with given value.
     *
     * @param property the property to add
     * @param value    the value of the property
     * @return this token.
     * Adds a property with the given value. The property name will be "Property i" where i this the current number of
     * properties.
     *
     * @param value the value of the property.
     """
    def addProperty(self, value: str=None, name: str=None, index: int=None, token_property: str=None):
        if name is not None and value is not None:
            self._tokenProperties[TokenProperty(name=name, level=len(self._tokenProperties))] = value
            return self
        elif index is not None and token_property is not None:
            self._tokenProperties[TokenProperty(level=self._tokenProperties[index])] = token_property
            return None  # !!
        elif token_property is not None and value is not None:
            self._tokenProperties[token_property] = value
            return self
        elif value is not None:
            self._tokenProperties[TokenProperty(level=self._tokenProperties[len(self._tokenProperties)])] = value
            return None  # !!
        else:
            raise Exception("addPropertyException")

    """
     * Sorts the properties by property level and name.
     *
     * @return a list of sorted token properties.
    """
    def getSortedProperties(self) -> list:
        sorted_properties = list(sorted(self._tokenProperties.keys(), key=attrgetter('level', 'name')))
        return sorted_properties

    """
     * Returns a collection of all property values.
     *
     * @return a collection of all property values.
    """
    # See the getter above...

    """
     * Check whether any of the property values contains the given string.
     *
     * @param substring the string to check whether it is contained in any property value of this token.
     * @return true iff there exists on property of this token for which <code>substring</code> is a substring of the
     *         corresponding property value.

    OR

     * Check whether any of the property values of this token contains any of the strings in the given set of strings.
     *
     * @param substrings set of strings to check
     * @param wholeWord  should we check for complete words of is it enough for the given strings to be substrings of
     *                   the token value.
     * @return true iff a) if there is a property value equal to one of the strings in <code>substrings</code>
     *         (wholeword=true) or b) if there is a property value that contains one of the strings in
     *         <code>substrings</code> (wholeword=false).
    """
    def propertiesContain(self, substring: str=None, substrings: set=None, wholeWord: bool=None) -> bool:
        if substring is not None:
            for curr_property in self._tokenProperties.values():
                if substring in curr_property:
                    return True
            return False
        else:
            if substrings is not None and wholeWord is not None:
                for curr_property in self._tokenProperties.values():
                    for substr in substrings:
                        if re.match("\d+-\d+$", substr):  # Full string match in JAVA!
                            From, To = substr.split("-")
                            if int(From) <= curr_property <= int(To):
                                return True
                        elif (wholeWord and curr_property == substr) or substr in curr_property:
                            return True
            return False

    """
     * Checks whether the two tokens have the same index. (Hence equality is only defined through the position of the
     * token in the sentence.
     *
     * @param o the other token.
     * @return <code>index==((Token)o).index</code>
    """
    def __eq__(self, other):
        return other is not None and isinstance(other, self.__class__) and self._index == other.index

    """
     * Returns the index of the token.
     *
     * @return the index of the token.
    """
    def __hash__(self):
        return self.index

    """
     * Inserts all properties and values of the other token into this token. In case of clashes the value of the other
     * token is taken.
     *
     * @param token the token to merge with.
    """
    def merge(self, token):
        self._tokenProperties.update(token.tokenProperties)

    """
     * Compares the indices of both tokens.
     *
     * @param o the other token.
     * @return <code>index - o.getIndex()</code>
    """
    def compareTo(self, other):
        return self._index - other.index

    """
     * Returns a string representation of this token containing token index and properties.
     *
     * @return a string representation of this token.
    """
    def __str__(self):
        return "{0}:{1}".format(self._index, ", ".join(str(prop) for prop in self._tokenProperties))
