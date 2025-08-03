import sys
import pytest


import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leak_helper_gdb import *


def test_parse():
    pass


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-vv"]))
