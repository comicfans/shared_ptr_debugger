import click
from types import SimpleNamespace
import pytest
import sys
import tempfile
import time
import os
from pathlib import Path
import pexpect


def create_recording(gdb, init, binary, recording: Path):
    if os.path.exists(recording):
        os.unlink(recording)

    run_gdb(
        gdb,
        init,
        binary,
        [
            (
                f"break_leak_function {recording}",
                r"\(gdb\)",
            ),
            ("r", r"\[Inferior \d+ \(process \d+\) exited normally\]"),
        ],
    )

    assert os.path.exists(recording)


def stderr_no_output(f, exit):
    while not exit.exit:
        try:
            time.sleep(2)
            if os.path.getsize(f) == 0:
                continue
            return
        except FileNotFoundError:
            pass


def run_gdb_under_pytest(commands: list[str | tuple[str, str] | tuple[str, int]]):
    run_gdb(
        pytest.my_global_variable.gdb,
        pytest.my_global_variable.init,
        pytest.my_global_variable.binary,
        commands,
    )


def run_gdb(gdb, init, binary, commands: list[str | tuple[str, str] | tuple[str, int]]):
    os.environ["NO_COLOR"] = "1"

    stderr_log = tempfile.NamedTemporaryFile(delete=False).name

    print(f"binary is {binary}, gdb is {gdb}, stderr_log is {stderr_log}")
    shell_command = f'"{gdb}" --nh --nx -ix {init} {binary} 2>{stderr_log}'
    process = pexpect.spawn(
        "/bin/bash",
        ["-c", shell_command],
    )
    process.logfile = sys.stdout.buffer

    # exit = SimpleNamespace(exit=False)
    # thread = Thread(target=stderr_no_output, args=(stderr_log, exit))
    # thread.start()

    if binary:
        process.expect(f"Reading symbols from {binary}\.\.\.")
    else:
        process.expect("\(gdb\)")

    for command in commands:
        if isinstance(command, str):
            process.sendline(command)
            continue
        assert isinstance(command, tuple)

        process.sendline(command[0])

        if isinstance(command[1], str):
            process.expect(command[1])
        else:
            assert isinstance(command[1], int)
            time.sleep(command[1])

    process.sendline("q")
    process.expect(pexpect.EOF)
    # exit.exit = True
    # thread.join()

    if os.path.getsize(stderr_log) != 0:
        lines = open(stderr_log).read()
        raise ValueError(lines)


@click.command()
@click.option("--gdb", required=True, help="which gdb to test")
@click.option("--init", required=True, help="where to load gdb init")
@click.option("--binary", default="", help="which binary to test")
@click.option(
    "--recording",
    default=None,
    required=False,
    help="create leak recording for that binary, instead of run pytest",
)
def run_click(gdb, init, binary, recording):
    if recording:
        create_recording(gdb, init, binary, recording)
        return

    pytest.my_global_variable = SimpleNamespace(
        gdb=gdb, init=init, binary=binary, file=pytest.my_global_variable.file
    )
    sys.exit(pytest.main([pytest.my_global_variable.file, "-vv"]))


def run_pytest(file):
    pytest.my_global_variable = SimpleNamespace(file=file)
    run_click()


if __name__ == "__main__":
    run_click()
