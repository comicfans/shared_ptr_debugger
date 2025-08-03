import gdb

from .leak_helper_gdb import parse_file_functions, filter_shared_ptr


class ListLeakBreak(gdb.Command):
    def __init__(self):
        super(ListLeakBreak, self).__init__(
            "list_leak_break", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        lines = gdb.execute("info functions", from_tty, True).splitlines()

        df = parse_file_functions(lines)

        filtered = filter_shared_ptr(df)

        if arg is not None:
            filtered.to_csv(arg)
        else:
            for row in filtered["function"]:
                print(row)


class AutoTrace(gdb.Command):
    def __init__(self):
        super(AutoTrace, self).__init__(
            "auto_trace", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        pass


ListLeakBreak()
