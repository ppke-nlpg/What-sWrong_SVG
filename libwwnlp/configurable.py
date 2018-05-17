#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Support for configurable objects, inspired by a similar solution found in
Google's seq2seq library at https://github.com/google/seq2seq.
"""

import yaml
import copy


def params_at_path(params, path):
    """Return params at a certain path.

    Args:
        params: A dict with string keys.
        path: String of subparams or set of subparams
    """
    if isinstance(path, str):
        path = {path}

    return {key_sub: val for (key_main, key_sub), val in
            ((key.split('.', maxsplit=1), val) for key, val in params.items())
            if key_main in path}


class Configurable:
    """Base class for objects configurable by a parameter dict.
    """

    def __init__(self, params):
        if params:
            self.params = self.parse_params(params)
        else:
            self.params = self.default_params()

    @staticmethod
    def default_params():
        raise NotImplementedError

    def parse_params(self, params):
        """Parse parameters.

        Args: 
            params: A dict or a yaml string specifying a dict. default_params:
                Default parameters as a dict.

        Returns:
            dict: The actual parameters that contain both the given params and the
                non-overridden defaults.
        """
        result = copy.deepcopy(self.default_params())
        parsed_params = {}
        if params:
            if isinstance(params, dict):
                parsed_params = params
            else:
                parsed_params = yaml.load(params)
                for key, value in parsed_params.items():
                    if key in self.default_params():
                        parsed_params[key] = value
                    else:
                        raise ValueError('Config key {0} is not allowed for class {1}.'.format(key, type(self)))
        return result.update(parsed_params)
