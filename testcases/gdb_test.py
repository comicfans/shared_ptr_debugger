import click
from types import SimpleNamespace
import run_under_gdb
import pytest


def test_default_run():
    run_under_gdb.run(
        pytest.my_global_variable.gdb,
        pytest.my_global_variable.init,
        pytest.my_global_variable.binary,
        [],
    )


@click.command()
@click.option("--gdb", required=True, help="which gdb to test")
@click.option("--init", required=True, help="where to load gdb init")
@click.option("--binary", required=True, help="which binary to test")
def main(gdb, init, binary):
    pytest.my_global_variable = SimpleNamespace(gdb=gdb, init=init, binary=binary)
    pytest.main([__file__, "-vv"])


if __name__ == "__main__":
    main()
