import sys
import time
from types import SimpleNamespace
import os
import pexpect
from threading import Thread


def stderr_no_output(f, exit):
    while not exit.exit:
        try:
            time.sleep(2)
            if os.path.getsize(f) == 0:
                continue

            for line in open(f):
                print(f"GDB_STDERR:{line}", flush=True)
            os._exit(1)
        except FileNotFoundError:
            pass


def run(gdb, init, binary, commands):
    os.environ["NO_COLOR"] = "1"
    print(f"binary is {binary}, gdb is {gdb}")

    stderr_log = f"{os.path.basename(binary)}.log"
    os.remove(stderr_log)

    shell_command = f'"{gdb}" --nh --nx -ix {init} {binary} 2>{stderr_log}'
    process = pexpect.spawn(
        "/bin/bash",
        ["-c", shell_command],
    )
    process.logfile = sys.stdout.buffer

    exit = SimpleNamespace(exit=False)
    thread = Thread(target=stderr_no_output, args=(stderr_log, exit))
    thread.start()

    process.expect(f"Reading symbols from {binary}\.\.\.")

    for line in commands:
        process.sendline(line)

    process.sendline("q")
    process.expect(pexpect.EOF)
    exit.exit = True
    thread.join()

    pass
