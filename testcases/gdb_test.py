import click
import re
import os
import pexpect
import subprocess
import time
from subprocess import Popen, PIPE, STDOUT
from queue import Queue, Empty
from threading import Thread


def stderr_no_output(line):
    print(f"stderr has output: -{line}-", flush=True)
    os._exit(1)


class ReadPipe:
    def __init__(self, pipe, callback=None):
        self.queue = Queue()
        self.pipe = pipe

        if callback is None:
            callback = self.append_queue
        self.callback = callback
        self.thread = Thread(target=self.run)
        self.thread.start()

    def append_queue(self, line):
        self.queue.put(line)

    def readline(self):
        try:
            line = self.queue.get_nowait()  # or q.get(timeout=.1)
            return line
        except Empty:
            return None

    def read_until(self, regex_str):
        regex = re.compile(regex_str)
        while True:
            line = self.readline()
            if not line:
                continue
            if regex.search(line):
                print(f"matched {line}")
                return
            print(line)
            continue
            pass

    def run(self):
        for line in iter(self.pipe.readline, b""):
            self.callback(line)

    def join(self):
        self.thread.join()


@click.command()
@click.option("--gdb", help="which gdb to test")
@click.option("--binary", help="which binary to test")
def main(gdb, binary):
    print(f"binary is {binary}, gdb is {gdb}")

    process = subprocess.Popen(
        [gdb, "-nh", "-nx"], stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True
    )

    std_out = ReadPipe(process.stdout)
    std_err = ReadPipe(process.stderr, stderr_no_output)

    std_out.read_until(f"Reading symbols from {binary}\.\.\.")
    # std_out.read_until(
    #    'Type "apropos word" to search for commands related to "word"...'
    # )
    # process.stdin.write("r\n")

    # std_out.read_until("Inferior 1 (process \d+) exited normally]")
    print("want to exit", flush=True)
    process.stdin.write("q\n\r")

    print("begin wait ")
    process.wait()
    print("wait finished")

    pass


if __name__ == "__main__":
    main()
