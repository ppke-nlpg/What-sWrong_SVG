#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


"""
 * A Pair is a typed pair of objects.
 *
 * @author Sebastian Riedel
"""
class Pair:

    """
     * Creates a pair with the given arguments
     *
     * @param arg1 First argument.
     * @param arg2 Second argument.
    """
    def __init__(self, A1, A2):
        self.arg1 = A1
        self.arg2 = A2

    """
     * Checks whether both arguments are equal.
     *
     * @param o the other pair.
     * @return true iff both arguments are equal.
    """
    def __eq__(self, other):
        if(other is None or self.__class__() != other.__class__()):
            return False
        if self.arg1 is not None and self.arg1 != other.arg1:
            return False
        if self.arg2 is not None and self.arg2 != other.arg2:
            return False
        return True

    """
     * Returns a hashcode based on both arguments.
     *
     * @return a hashcode based on both arguments.
    """
    def __hash__(self):
        if self.arg1 is not None:
            result = self.arg1.hash()
        else:
            result = 0
        if self.arg2 is not None:
            result = 31 * result + self.arg2.hash()
        return result

    """
     * Returns ([arg1],[arg2]) where [arg1] is replaced by the value of the first argument and [arg2] replaced by the
     * value of the second argument.
     *
     * @return the string "([arg1],[arg2])".
    """
    def __str__(self):
        return "(" + self.arg1 + ", " + self.arg2 +")"