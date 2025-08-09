from .leak_helper_gdb import (
    AllRecords,
)
import networkx as nx


def analysis(records_df) -> nx.Graph:
    grouped = records_df.groupby("id")
