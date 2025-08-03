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

    for expect_type in ["add_ref_copy", "add_ref_lock_nothrow", "destroy", "release"]:
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
        "/usr/include/c++/13/bits/exception.h": {
            62: "void std::exception::exception()"
        },
        "/usr/include/c++/13/bits/shared_ptr.h": {
            414: "std::shared_ptr<int> &std::shared_ptr<int>::operator=(std::shared_ptr<int> const&)",
            204: "void std::shared_ptr<int>::shared_ptr(std::shared_ptr<int> const&)",
            359: "void std::shared_ptr<int>::shared_ptr(std::shared_ptr<int>&&)",
            535: "void std::shared_ptr<int>::shared_ptr(std::weak_ptr<int> const&, std::nothrow_t)",
            214: "void std::shared_ptr<int>::shared_ptr<int, void>(int*)",
            380: "void std::shared_ptr<int>::shared_ptr<int, void>(std::weak_ptr<int> const&)",
            175: "void std::shared_ptr<int>::~shared_ptr()",
        },
        "/usr/include/c++/13/bits/shared_ptr_base.h": {
            151: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_add_ref_copy()",
            268: "bool std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_add_ref_lock_nothrow()",
            143: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_destroy()",
            226: "long std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_get_use_count() const",
            317: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release()",
            172: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release_last_use()",
            198: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release_last_use_cold()",
            203: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_weak_add_ref()",
            208: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_weak_release()",
            129: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_Sp_counted_base()",
            133: "void std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::~_Sp_counted_base()",
            431: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_M_destroy()",
            427: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_M_dispose()",
            435: "void *std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)",
            423: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::_Sp_counted_ptr(int*)",
            419: "void std::_Sp_counted_ptr<int*, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr()",
            1105: "long std::__shared_count<(__gnu_cxx::_Lock_policy)2>::_M_get_use_count() const",
            1097: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::_M_swap(std::__shared_count<(__gnu_cxx::_Lock_policy)2>&)",
            908: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count()",
            1074: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count(std::__shared_count<(__gnu_cxx::_Lock_policy)2> const&)",
            1241: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count(std::__weak_count<(__gnu_cxx::_Lock_policy)2> const&)",
            1251: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count(std::__weak_count<(__gnu_cxx::_Lock_policy)2> const&, std::nothrow_t)",
            913: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count<int*>(int*)",
            927: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::__shared_count<int*>(int*, std::integral_constant<bool, false>)",
            1082: "std::__shared_count<(__gnu_cxx::_Lock_policy)2> &std::__shared_count<(__gnu_cxx::_Lock_policy)2>::operator=(std::__shared_count<(__gnu_cxx::_Lock_policy)2> const&)",
            1068: "void std::__shared_count<(__gnu_cxx::_Lock_policy)2>::~__shared_count()",
            1765: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::_M_enable_shared_from_this_with<int, int>(int*)",
            1462: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr()",
            1522: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr(std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2> const&)",
            1531: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr(std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>&&)",
            1731: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr(std::__weak_ptr<int, (__gnu_cxx::_Lock_policy)2> const&, std::nothrow_t)",
            1468: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr<int, void>(int*)",
            1547: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::__shared_ptr<int, void>(std::__weak_ptr<int, (__gnu_cxx::_Lock_policy)2> const&)",
            1523: "std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2> &std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::operator=(std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2> const&)",
            1641: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::reset()",
            1524: "void std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2>::~__shared_ptr()",
            95: "void std::__throw_bad_weak_ptr()",
            1146: "void std::__weak_count<(__gnu_cxx::_Lock_policy)2>::__weak_count(std::__shared_count<(__gnu_cxx::_Lock_policy)2> const&)",
            1164: "void std::__weak_count<(__gnu_cxx::_Lock_policy)2>::~__weak_count()",
            2015: "void std::__weak_ptr<int, (__gnu_cxx::_Lock_policy)2>::__weak_ptr<int, void>(std::__shared_ptr<int, (__gnu_cxx::_Lock_policy)2> const&)",
            1993: "void std::__weak_ptr<int, (__gnu_cxx::_Lock_policy)2>::~__weak_ptr()",
            85: "void std::bad_weak_ptr::bad_weak_ptr()",
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
