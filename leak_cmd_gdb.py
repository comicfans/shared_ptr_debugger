import gdb

import leak_cmd_gdb


class ListLeakBreak(gdb.Command):
    def __init__(self):
        super(ListLeakBreak, self).__init__(
            "list_leak_break", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        lines = gdb.execute("info functions", from_tty, True)

        print(len(lines))


class AutoTrace(gdb.Command):
    def __init__(self):
        super(AutoTrace, self).__init__(
            "auto_trace", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        pass


ListLeakBreak()
