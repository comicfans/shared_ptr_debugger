import click
import pickle
import os
from types import SimpleNamespace
import run_under_gdb
import pytest
import sys


def test_save_recording(request):
    pwd = os.getcwd()
    output = f"{pwd}/{request.node.name}.sqlite3"

    if os.path.exists(output):
        os.unlink(output)

    run_under_gdb.run(
        pytest.my_global_variable.gdb,
        pytest.my_global_variable.init,
        pytest.my_global_variable.binary,
        [f"break_leak_function {output}", "r"],
    )

    assert os.path.exists(output)


def test_default_import():
    run_under_gdb.run(
        pytest.my_global_variable.gdb,
        pytest.my_global_variable.init,
        pytest.my_global_variable.binary,
        [],
    )


def test_hook_functions(request):
    output = f"{request.node.name}.pickle"
    if os.path.exists(output):
        os.unlink(output)

    run_under_gdb.run(
        pytest.my_global_variable.gdb,
        pytest.my_global_variable.init,
        pytest.my_global_variable.binary,
        [
            f"list_leak_break {output}",
        ],
    )
    assert os.path.exists(output)
    readback = pickle.load(open(output, "rb"))

    common_df = readback["common"]
    assert len(common_df) != 0
    typed_df = readback["typed"]
    assert len(typed_df) != 0


@click.command()
@click.option("--gdb", required=True, help="which gdb to test")
@click.option("--init", required=True, help="where to load gdb init")
@click.option("--binary", required=True, help="which binary to test")
def main(gdb, init, binary):
    pytest.my_global_variable = SimpleNamespace(gdb=gdb, init=init, binary=binary)
    sys.exit(pytest.main([__file__, "-vv"]))


if __name__ == "__main__":
    main()
