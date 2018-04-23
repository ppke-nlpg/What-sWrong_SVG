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
    result = copy.deepcopy(default_params)
    if isinstance(params, dict):
        parsed_params = params
    else:
        parsed_params = yaml.load(params)
    result.update(parsed_params)
    return result
    

class Configurable:
    """Base class for objects configurable by a parameter dict.
    """

    def __init__(self, params):
        self.params = parse_params(params, self.default_params())

    def default_params():
        raise NotImplementedError

    
        
        

    
