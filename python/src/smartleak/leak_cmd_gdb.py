import gdb
import pickle

from .leak_helper_gdb import parse_file_functions, filter_shared_ptr


def gdb_function_filter_shared(from_tty):
    lines = gdb.execute("info functions", from_tty, True).splitlines()
    df = parse_file_functions(lines)
    filtered = filter_shared_ptr(df)
    return filtered


class TraceContext:
    def __init__(self, template_type):
        self.template_type = template_type
        pass


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
                print(type)
                for function in value["function"]:
                    print(function)


class TypedLeakTraceBreak(gdb.Breakpoint):
    def __init__(self, trace_context, **kwargs):
        super().__init__(**kwargs)
        self.trace_context = trace_context

    def stop(self, **kwargs):
        return False


class CommonLeakTraceBreak(gdb.Breakpoint):
    def __init__(self, trace_context, **kwargs):
        super().__init__(**kwargs)
        self.trace_context = trace_context

    def stop(self):
        return False


class BreakLeakFunction(gdb.Command):
    def __init__(self):
        super(BreakLeakFunction, self).__init__(
            "break_leak_function", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION
        )

    def invoke(self, arg, from_tty):
        if arg:
            print("try load")
            with open(arg, "rb") as f:
                filtered = pickle.load(f)
        else:
            print("analysis")
            filtered = gdb_function_filter_shared(from_tty)

        if filtered is None or len(filtered) == 0:
            print("no valid function found")
            return

        for type, value in filtered.items():
            print(type)
            for function in value["function"]:
                print(function)
                break_spec = " ".join(function.split(" ")[1:])
                if type == "common":
                    CommonLeakTraceBreak(break_spec)
                else:
                    TypedLeakTraceBreak(break_spec)


ListLeakBreak()
BreakLeakFunction()
