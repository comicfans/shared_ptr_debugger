import pickle
import os
import pytest

from context import run_pytest, run_gdb_under_pytest


def test_hook_functions(request):
    binary_name = os.path.basename(pytest.my_global_variable.binary)
    output = f"{binary_name}_{request.node.name}.pickle"
    if os.path.exists(output):
        os.unlink(output)

    run_gdb_under_pytest(
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


if __name__ == "__main__":
    run_pytest(file=__file__)
