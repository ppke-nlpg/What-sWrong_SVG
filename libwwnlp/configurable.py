#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Support for configurable objects, inspired by a similar solution found in
Google's seq2seq library at https://github.com/google/seq2seq.
"""

import yaml
import copy

def parse_params(params, default_params):
    """Merge params with default params
    
    Args:
        params: A dict or a yaml string specifying a dict.
        default_params: Default parameters as a dict.
    """
    if not params:
        return default_params
    else:
        result = copy.deepcopy(default_params)
        if isinstance(params, dict):
            parsed_params = params
        else:
            parsed_params = yaml.load(params)
        result.update(parsed_params)
        return result

    
def params_at_path(params, path):
    """Return params at a certain path.

    Args:
        params: A dict with string keys.
    """
    return {key[len(path)+1:]: val for key, val in params.items() if key.startswith(path+".")}


class Configurable:
    """Base class for objects configurable by a parameter dict.
    """

    def __init__(self, params):
        if params:
            self.params = parse_params(params, self.default_params())
        else:
            self.params = self.default_params()

    @staticmethod
    def default_params():
        raise NotImplementedError

    
        
        

    
