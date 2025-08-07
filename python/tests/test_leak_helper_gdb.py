from smartleak.leak_helper_gdb import parse_file_functions, filter_shared_ptr


def test_parse_file_functions_incorrect_str_correct_type(request):
    rootdir = request.config.rootdir
    lines = open(rootdir / "tests" / "input.txt").read()
    df = parse_file_functions(lines)
    filtered = filter_shared_ptr(df)  # noqa: F841


def test_filter_shared_ptr(request):
    rootdir = request.config.rootdir
    lines = open(rootdir / "tests" / "input.txt").readlines()
    df = parse_file_functions(lines)
    filtered = filter_shared_ptr(df)

    typed = filtered["typed"]

    for expect_type in ["int"]:
        assert len(typed[typed["template_type"] == expect_type]) != 0

    common = filtered["common"]

    for expect_type in [
        # "add_ref_copy", "add_ref_lock_nothrow",
        "destroy",
        "release",
    ]:
        assert len(common[common["function_type"] == expect_type]) != 0


def test_parse_file_functions_empty_correct_type():
    lines = []
    df = parse_file_functions(lines)
    filtered = filter_shared_ptr(df)  # noqa: F841


def test_parse_file_functions(request):
    rootdir = request.config.rootdir
    lines = open(rootdir / "tests" / "input.txt").readlines()
    df = parse_file_functions(lines)
    expect = {
        "/home/xwang/project/smartleak/testcases/no_leak/local_int.cpp": {
            3: "int main()"
        },
        "/usr/include/c++/13/bits/shared_ptr_base.h": {
            143: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_destroy()",
            317: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release()",
            172: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release_last_use()",
            198: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release_last_use_cold()",
            129: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_Sp_counted_base()",
            133: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::~_Sp_counted_base()",
            431: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_M_destroy()",
            427: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_M_dispose()",
            435: "void *std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)",
            423: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_Sp_counted_ptr(int*)",
            419: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr()",
            913: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count<int*>(int*)",
            927: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count<int*>(int*, std::integral_constant<bool, false>)",
            1068: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::~__shared_count()",
            1765: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::_M_enable_shared_from_this_with<int, int>(int*)",
            1468: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr<int, void>(int*)",
            1524: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::~__shared_ptr()",
        },
    }

    for file, line_func in expect.items():
        for line, func in line_func.items():
            all_match = (
                (df["file"] == file)
                & (df["line_number"] == line)
                & (df["function"] == func)
            )
            assert all_match.sum() == 1
