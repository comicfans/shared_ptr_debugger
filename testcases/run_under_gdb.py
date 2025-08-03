import sys
import tempfile
import time
import os
import pexpect


def stderr_no_output(f, exit):
    while not exit.exit:
        try:
            time.sleep(2)
            if os.path.getsize(f) == 0:
                continue
            return
        except FileNotFoundError:
            pass


def run(gdb, init, binary, commands):
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

    process.expect(f"Reading symbols from {binary}\.\.\.")

    for line in commands:
        process.sendline(line)

    process.sendline("q")
    process.expect(pexpect.EOF)
    # exit.exit = True
    # thread.join()

    if os.path.getsize(stderr_log) != 0:
        lines = open(stderr_log).read()
        raise ValueError(lines)
