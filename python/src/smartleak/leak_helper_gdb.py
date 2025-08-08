import re
import sqlite3
import json
from typing import Any
from collections import defaultdict
from itertools import chain

import pandas as pd


def parse_file_functions(lines) -> pd.DataFrame:
    file_header = None

    file_regex = re.compile(r"File (.*):")
    number_func = re.compile(r"(\d+):\s*(.*);")

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


def filter_shared_ptr(df: pd.DataFrame) -> dict[str : pd.DataFrame]:
    # catelog all function to common breakpoints and typed breakpoints
    #

    func_regex = dict(
        copy_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr\(std::shared_ptr<\1> const&\)$",
        move_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr\(std::shared_ptr<\1>&&\)$",
        from_row_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr<.+, void>\(\1\*\)$",
        from_weak_constructor=r"^void std::shared_ptr<(.+)>::shared_ptr<.+, void>\(std::weak_ptr<\1> const&\)$",
        destructor=r"^void std::shared_ptr<(.+)>::~shared_ptr()$",
        assign_operator=r"^std::shared_ptr<(.+)> &std::shared_ptr<\1>::operator=\(std::shared_ptr<\1> const&\)$",
    )

    typed_df = []
    for function_type, regex in func_regex.items():
        this_df = df[df["function"].str.match(regex)].copy()

        if len(this_df) == 0:
            continue

        this_df["function_type"] = function_type
        capture_groups = this_df["function"].str.extract(regex)

        this_df["template_type"] = capture_groups[0]
        typed_df.append(this_df)

    common_regex = {
        "add_ref_copy": r"^void std::_Sp_counted_base<.*>::_M_add_ref_copy\(\)$",
        "add_ref_lock_nothrow": r"^bool std::_Sp_counted_base<.*>::_M_add_ref_lock_nothrow\(\)$",
        "destroy": r"^void std::_Sp_counted_base<.*>::_M_destroy\(\)$",
        "release": r"^void std::_Sp_counted_base<.*>::_M_release\(\)$",
    }

    common_df = []
    for type, regex in common_regex.items():
        this_df = df[df["function"].str.match(regex)].copy()

        if len(this_df) == 0:
            continue

        this_df["function_type"] = type
        common_df.append(this_df)

    if len(typed_df) == 0:
        typed = df.iloc[[]].copy()
        typed["function_type"] = ""
        typed["template_type"] = ""
    else:
        typed = pd.concat(typed_df, ignore_index=True)

    if len(common_df) == 0:
        common = df.iloc[[]].copy()
        common["function_type"] = ""
    else:
        common = pd.concat(common_df, ignore_index=True)

    return dict(typed=typed, common=common)


class ReusableId:
    """a unique id generator for resuable objects

    for thread/mem_address, they can be recycled and reused
    we need to distinguish them during whole program lifetime

    """

    def __init__(self):
        self.alive = dict()
        self.recycled = dict()

    def is_alive(self, resuable) -> bool:
        return resuable in self.alive

    def unique_by(self, resuable) -> tuple[int, Any]:
        try_alive = self.alive.get(resuable)

        if try_alive:
            return try_alive

        # not alive, check if duplicate recycled
        duplicate = self.recycled.get(resuable)
        if not duplicate:
            self.alive[resuable] = 0
            return (0, resuable)

        # duplicate with existing
        this_counter = duplicate + 1
        self.alive[resuable] = this_counter
        return (this_counter, resuable)

    def destroy_resuable(self, resuable):
        this_counter = self.alive[resuable]

        if this_counter == 0:
            assert resuable not in self.recycled, "recycle a resuable that is not alive"
        else:
            assert this_counter == self.recycled[resuable] + 1, (
                "recycle a resuable that is not the last alive"
            )

        self.recycled[resuable] = this_counter
        del self.alive[resuable]


def db_init(file: str):
    con = sqlite3.connect(file)
    cur = con.cursor()
    # TODO refactor to meta + event (foreign id only)
    cur.execute("CREATE TABLE IF NOT EXISTS events (process, info)")
    cur.close()
    con.close()


class SingleRunRecords:
    """
    records for one pid
    """

    def __init__(self, id, db_file):
        self.id = id
        db_init(db_file)
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def append_event(self, info: dict[str, Any]) -> None:
        json_string = json.dumps(info)

        with self.conn:
            self.conn.execute(
                "INSERT INTO events (process, info) VALUES (?,?)",
                (json.dumps(self.id), json_string),
            )

        pass

    def close(self):
        self.cur.close()
        self.conn.close()


class AllRecords:
    def __init__(self, db_file):
        self.db_file = db_file
        self.runs = {}

    def close(self):
        for key, value in self.runs.items():
            value.close()

    def by(self, id) -> SingleRunRecords:
        if id not in self.runs:
            self.runs[id] = SingleRunRecords(id, self.db_file)
        return self.runs[id]

    @staticmethod
    def load(db_file):
        conn = sqlite3.connect(db_file)
        df = pd.read_sql_query("select * from events", conn)
        df["info"] = df["info"].apply(json.loads)
        conn.close()
        return df
