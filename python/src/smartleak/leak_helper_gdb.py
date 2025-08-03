import re
from itertools import chain
from collections import defaultdict
import pandas as pd


def parse_file_functions(lines) -> pd.DataFrame:
    file_header = None

    file_regex = re.compile(r"File (.*):")
    number_func = re.compile(r"(\d+): *(.*);")

    file_funcs = defaultdict(list)

    for file_line in lines:
        line = file_line.strip()

        if file_header is None:
            file_match = file_regex.search(line)
            if file_match:
                file_header = file_match[1]
            continue

        matched = number_func.search(line.strip())
        if not matched:
            file_header = None
            continue

        file_funcs[file_header].append((matched[1], matched[2]))
    return pd.DataFrame(
        data=dict(
            file=pd.Series(
                chain.from_iterable(
                    [key] * len(value) for key, value in file_funcs.items()
                ),
                dtype="string",
            ),
            line_number=pd.Series(
                chain.from_iterable(
                    [int(v[0]) for v in value] for value in file_funcs.values()
                ),
                dtype="int",
            ),
            function=pd.Series(
                chain.from_iterable(
                    [v[1] for v in value] for value in file_funcs.values()
                ),
                dtype="string",
            ),
        )
    )


# print(parse_file_functions(open("input.txt").readlines())["function"].to_list())


# df = parse_file_functions(open("input.txt").readlines())


def filter_shared_ptr(df: pd.DataFrame) -> pd.DataFrame:
    # TODO we can analysis these function from clang

    func_regex = dict(
        copy_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr\(std::shared_ptr<\1> const&\)$",
        move_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr\(std::shared_ptr<\1>&&\)$",
        from_row_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr<.+, void>\(\1\*\)$",
        from_weak_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr<.+, void>\(std::weak_ptr<\1> const&\)$",
        destructor=r"^void std::shared_ptr<(.+)>::~shared_ptr()$",
        assign_operator=r"^std::shared_ptr<(.+)> &std::shared_ptr<\1>::operator=\(std::shared_ptr<\1> const&\)$",
    )

    list_df = []
    for function_type, regex in func_regex.items():
        this_df = df[df["function"].str.match(regex)].copy()

        this_df["function_type"] = function_type
        capture_groups = this_df["function"].str.extract(regex)

        this_df["template_type"] = capture_groups[0]
        list_df.append(this_df)

    all_types = pd.concat(list_df, ignore_index=True)
    return all_types
