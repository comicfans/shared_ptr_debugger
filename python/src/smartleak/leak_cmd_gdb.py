import gdb
import pickle

from .leak_helper_gdb import (
    parse_file_functions,
    filter_shared_ptr,
    AllRecords,
)


def gdb_function_filter_shared(from_tty):
    lines = gdb.execute("info functions", from_tty, True).splitlines()
    df = parse_file_functions(lines)
    filtered = filter_shared_ptr(df)
    return filtered


class ListLeakBreak(gdb.Command):
    def __init__(self):
        super(ListLeakBreak, self).__init__(
            "list_leak_break", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        filtered = gdb_function_filter_shared(from_tty)
        if arg:
            with open(arg, "wb") as f:
                pickle.dump(filtered, f)
        else:
            for type, value in filtered.items():
                print(f"{type}:")
                for function in value["function"]:
                    print(function)


class CommonBreak(gdb.Breakpoint):
    def __init__(self, all_records: AllRecords, info, **kwargs):
        super().__init__(**kwargs)
        self.all_records = all_records
        self.info = info

    def stop(self):
        inferior = gdb.selected_inferior()
        progspec = gdb.current_progspace()
        records = self.all_records.by(
            (progspec.executable_filename, inferior.num, inferior.pid)
        )

        records.append_event(self.info)
        return True


class TypedLeakTraceBreak(CommonBreak):
    def __init__(self, all_records, info, **kwargs):
        super().__init__(all_records, info, **kwargs)


class CommonLeakTraceBreak(CommonBreak):
    def __init__(self, all_records, info, **kwargs):
        super().__init__(all_records, info, **kwargs)


# gdb can debug multi process simultaneously  (even one program with multi instance)
# different program is distinguished by inferiors
# same program different instance is distinguished by inferior.num
# not started program only have inferiors, but no connections
ALL_RECORDS = None


class BreakLeakFunction(gdb.Command):
    def __init__(self):
        super(BreakLeakFunction, self).__init__(
            "break_leak_function", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        filtered = gdb_function_filter_shared(from_tty)

        if not filtered:
            print("no valid function found")
            return

        global ALL_RECORDS
        if ALL_RECORDS is not None:
            ALL_RECORDS.close()

        ALL_RECORDS = AllRecords(arg or "records.sqlite3")
        # TODO we need to check commands run before program start

        for type, value in filtered.items():
            for row in value.itertuples():
                info = row._asdict()
                break_spec = " ".join(info["function"].split(" ")[1:])

                if type == "common":
                    CommonLeakTraceBreak(ALL_RECORDS, info, spec=break_spec)
                else:
                    TypedLeakTraceBreak(ALL_RECORDS, info, spec=break_spec)


ListLeakBreak()
BreakLeakFunction()
