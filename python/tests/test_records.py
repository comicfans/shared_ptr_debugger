from smartleak.leak_helper_gdb import AllRecords
import os
import json
from unittest import TestCase


def test_all_record(request):
    db_file = f"{request.node.name}.sqlite3"
    if os.path.exists(db_file):
        os.unlink(db_file)
    all_records = AllRecords(db_file)

    info = dict(a=1, b=2)
    all_records.by(1234).append_event(info)
    all_records.close()

    loaded = AllRecords.load(db_file)

    assert len(loaded) == 1
    assert loaded.process[0] == json.dumps(1234)
    TestCase().assertEqual(loaded["info"][0], info)

    pass
