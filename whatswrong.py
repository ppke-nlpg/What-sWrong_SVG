#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Qt5GUI.GUIMain import main, test

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "DEBUG":
        filename = "malt.txt"
        if len(sys.argv) > 2:
            filename = sys.argv[2]
        test(filename)
        exit(1)
    else:
        main(sys.argv)
