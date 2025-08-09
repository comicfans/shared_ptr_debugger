from run_under_gdb import run_pytest, run_gdb_under_pytest


def test_default_import():
    run_gdb_under_pytest([])


if __name__ == "__main__":
    run_pytest(file=__file__)
